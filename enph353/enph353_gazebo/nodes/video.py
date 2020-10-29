#!/usr/bin/env python2

"""
Wrapper around cv2 video writer so that it can be used as a context manager
"""

import cv2


class VideoWriter(cv2.VideoWriter):
    """
    Extend cv2.VideoWriter to provide a context manager.
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        return False
