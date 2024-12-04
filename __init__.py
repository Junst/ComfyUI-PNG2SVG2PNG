from .node import *
from .install import *

# install the required packages
ensure_package()

NODE_CLASS_MAPPINGS = {
    "PNG2SVG2PNG" : PNG2SVG2PNGNode,
    }

__all__ = ['NODE_CLASS_MAPPINGS']
