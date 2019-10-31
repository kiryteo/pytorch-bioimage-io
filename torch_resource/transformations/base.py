
#
# TODO in a real lib we would want something similar to inferno's batch_function, ...
# functionality, but more flexible w.r.t implementing different dimensions.
#

class IndependentTransformation:
    """ Transformation that can be applied to all input tensors independently.
    """
    def __init__(self, apply_to):
        self.apply_to = apply_to

    def __call__(self, *tensors):
        ret = [self.apply_transformation(x) if ii in self.apply_to else x
               for ii, x in enumerate(tensors)]
        return ret


class SynchronizedTransformation:
    """ Transformation for which application to all tensors is synchronized.
    This means, some state must be known before applying it to the tensors,
    e.g. the degree before a random rotation
    """
    def __init__(self, apply_to):
        self.apply_to = apply_to

    def __call__(self, *tensors):
        self.set_next_state()
        ret = [self.apply_transformation(x) if ii in self.apply_to else x
               for ii, x in enumerate(tensors)]
        return ret


def apply_transformations(transformations, *tensors):
    """ Helper function to apply a list of transformations to input tensors.
    """
    if not all(callable(trafo) for trafo in transformations):
        raise ValueError("Expect iterable with callables")
    for trafo in transformations:
        tensors = trafo(*tensors)
    return tensors