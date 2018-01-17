#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""MLP layer (chainer)."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import chainer
from chainer import functions as F
from chainer import links as L


class LinearND(chainer.Chain):

    def __init__(self, *size, bias=True, dropout=0, use_cuda=False):
        """
        A chainer.links.Linear layer modified to accept ND arrays.
            The function treats the last dimension of the input
            as the hidden dimension.
        Args:
            size ():
            bias (bool, optional):
            dropout (float, optional):
            use_cuda (bool, optional): if True, use GPUs
        """
        super(LinearND, self).__init__()

        self.dropout = dropout

        with self.init_scope():
            self.fc = L.Linear(*size,
                               nobias=not bias,
                               initialW=None,
                               initial_bias=None)
            if use_cuda:
                self.fc.to_gpu()

    def __call__(self, xs):
        size = list(xs.shape)
        outputs = F.reshape(xs, (np.prod(size[:-1]), size[-1]))
        outputs = self.fc(outputs)
        if self.dropout > 0:
            outputs = F.dropout(outputs, ratio=self.dropout)
        size[-1] = outputs.shape[-1]
        return F.reshape(outputs, size)