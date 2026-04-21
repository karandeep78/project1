"""
Compatibility shim for loading older scikit-learn models
This patches sys.modules to include sklearn.ensemble._gb_losses for backward compatibility
and fixes attribute issues with DecisionTreeRegressor
"""
import sys
import types

# Create a mock _gb_losses module and inject it into sys.modules
# This must be done before pickle tries to load the model
_gb_losses_module = types.ModuleType('sklearn.ensemble._gb_losses')

# Create mock classes that might be needed
# These are minimal stubs - the actual model should work if the classes exist
class MockLoss:
    """Mock loss class for compatibility"""
    pass

# Add common loss classes that older models might reference
_gb_losses_module.BinomialDeviance = MockLoss
_gb_losses_module.MultinomialDeviance = MockLoss
_gb_losses_module.ExponentialLoss = MockLoss
_gb_losses_module.LeastSquaresError = MockLoss
_gb_losses_module.LeastAbsoluteError = MockLoss
_gb_losses_module.HuberLossFunction = MockLoss
_gb_losses_module.QuantileLossFunction = MockLoss

sys.modules['sklearn.ensemble._gb_losses'] = _gb_losses_module

# Also ensure sklearn.ensemble has the attribute
if 'sklearn.ensemble' in sys.modules:
    sklearn_ensemble = sys.modules['sklearn.ensemble']
    sklearn_ensemble._gb_losses = _gb_losses_module
else:
    # Pre-import sklearn.ensemble to set it up
    import sklearn.ensemble
    sklearn.ensemble._gb_losses = _gb_losses_module

# Patch DecisionTreeRegressor to add monotonic_cst attribute for older models
def patch_tree_estimators(estimator):
    """Recursively patch tree estimators to add missing monotonic_cst attribute and fix loss objects"""
    from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
    from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
    
    # Try to import loss classes from new location (sklearn 1.5+)
    try:
        from sklearn._loss.loss import HalfBinomialLoss, HalfMultinomialLoss, HalfSquaredError
        from sklearn._loss.loss import HalfAbsoluteError, HalfPoissonLoss, HalfGammaLoss, HalfTweedieLoss
        NEW_LOSS_API = True
    except ImportError:
        NEW_LOSS_API = False
    
    def add_monotonic_cst(obj):
        """Add monotonic_cst attribute if missing"""
        if isinstance(obj, (DecisionTreeRegressor, DecisionTreeClassifier)):
            if not hasattr(obj, 'monotonic_cst'):
                obj.monotonic_cst = None
    
    # Fix loss object for GradientBoosting models
    if isinstance(estimator, (GradientBoostingClassifier, GradientBoostingRegressor)):
        if hasattr(estimator, '_loss') and isinstance(estimator._loss, MockLoss):
            # Reconstruct the loss object based on the model's loss parameter
            loss_name = getattr(estimator, 'loss', 'deviance')
            n_classes = getattr(estimator, 'n_classes_', None)
            
            try:
                if NEW_LOSS_API:
                    # Debug: print what we're doing
                    import sys
                    if hasattr(sys, '_getframe'):
                        print(f"DEBUG: Patching loss for {type(estimator).__name__}, loss={loss_name}, n_classes={n_classes}", file=sys.stderr)
                    # Use new sklearn 1.5+ loss API
                    if isinstance(estimator, GradientBoostingClassifier):
                        if loss_name == 'deviance' or loss_name == 'log_loss':
                            if n_classes == 2:
                                estimator._loss = HalfBinomialLoss()
                            else:
                                estimator._loss = HalfMultinomialLoss(n_classes)
                        elif loss_name == 'exponential':
                            # Exponential loss is deprecated, use log_loss instead
                            estimator._loss = HalfBinomialLoss() if n_classes == 2 else HalfMultinomialLoss(n_classes)
                    else:  # GradientBoostingRegressor
                        if loss_name == 'ls' or loss_name == 'squared_error':
                            estimator._loss = HalfSquaredError()
                        elif loss_name == 'lad' or loss_name == 'absolute_error':
                            estimator._loss = HalfAbsoluteError()
                        elif loss_name == 'huber':
                            # Huber loss needs alpha parameter
                            alpha = getattr(estimator, 'alpha', 0.9)
                            from sklearn._loss.loss import HalfHuberLoss
                            estimator._loss = HalfHuberLoss(quantile=alpha)
                        elif loss_name == 'quantile':
                            alpha = getattr(estimator, 'alpha', 0.5)
                            from sklearn._loss.loss import HalfPinnedHuberLoss
                            estimator._loss = HalfPinnedHuberLoss(quantile=alpha)
                else:
                    # Fallback: try to get loss from model's _get_loss method if available
                    try:
                        estimator._loss = estimator._get_loss()
                    except:
                        pass
            except Exception as e:
                # If setting loss fails, try alternative approach
                import warnings
                warnings.warn(f"Could not set loss object: {e}")
                pass
    
    if hasattr(estimator, 'estimators_'):
        # This is an ensemble (like GradientBoostingClassifier)
        if hasattr(estimator.estimators_, 'shape'):
            # estimators_ is a 2D array (n_classes x n_estimators for classification)
            for i in range(estimator.estimators_.shape[0]):
                for j in range(estimator.estimators_.shape[1]):
                    tree = estimator.estimators_[i, j]
                    add_monotonic_cst(tree)
        elif isinstance(estimator.estimators_, (list, tuple)):
            # estimators_ is a list/tuple
            for tree in estimator.estimators_:
                add_monotonic_cst(tree)
                if hasattr(tree, 'estimators_'):
                    patch_tree_estimators(tree)
    else:
        # Direct tree estimator
        add_monotonic_cst(estimator)
    
    return estimator
