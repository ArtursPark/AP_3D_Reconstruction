from optimization.src.optimizer_data_interface import OptimizerDataInterface


class BundleAdjustentOptimizerInterface:
    def __init__(self) -> None:
        self.__m_data = None

    def compute(self, in_optimizer_data_interface: OptimizerDataInterface):
        raise NotImplementedError("BundleAdjustentOptimizerInterface::compute()")


class BundleAdjustmentOptimizer(BundleAdjustentOptimizerInterface):
    def __init__(self) -> None:
        super().__init__()

    def compute(self, in_optimizer_data_interface: OptimizerDataInterface):
        raise NotImplementedError("BundleAdjustentOptimizerInterface::compute()")
