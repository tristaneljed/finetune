import tensorflow as tf

from finetune.base import BaseModel
from finetune.target_encoders import RegressionEncoder
from finetune.network_modules import regressor


class Regressor(BaseModel):

    def featurize(self, X, max_length=None):
        """
        Embeds inputs in learned feature space. Can be called before or after calling :meth:`finetune`.

        :param X: list or array of text to embed.
        :param max_length: the number of tokens to be included in the document representation.
                           Providing more than `max_length` tokens as input will result in truncation.
        :returns: np.array of features of shape (n_examples, embedding_size).
        """
        return self._featurize(X, max_length=max_length)

    def predict(self, X, max_length=None):
        """
        Produces a list of most likely class labels as determined by the fine-tuned model.

        :param X: list or array of text to embed.
        :param max_length: the number of tokens to be included in the document representation.
                           Providing more than `max_length` tokens as input will result in truncation.
        :returns: list of class labels.
        """
        super().predict(X, max_length=max_length)

    def predict_proba(self, X, max_length=None):
        """
        Produces a probability distribution over classes for each example in X.

        :param X: list or array of text to embed.
        :param max_length: the number of tokens to be included in the document representation.
                           Providing more than `max_length` tokens as input will result in truncation.
        :returns: list of dictionaries.  Each dictionary maps from a class label to its assigned class probability.
        """
        raise AttributeError("`Regressor` model does not support `predict_proba`.")

    def finetune(self, X, Y=None, batch_size=None):
        """
        :param X: list or array of text.
        :param Y: floating point targets
        :param batch_size: integer number of examples per batch. When N_GPUS > 1, this number
                           corresponds to the number of training examples provided to each GPU.
        """
        return super().finetune(X, Y=Y, batch_size=batch_size)

    def _target_encoder(self):
        return RegressionEncoder()

    def _target_model(self, featurizer_state, targets, n_outputs, train=False, reuse=None, **kwargs):
        return regressor(
            hidden=featurizer_state['features'],
            targets=targets, 
            n_targets=n_outputs,
            dropout_placeholder=self.do_dropout,
            config=self.config,
            train=train, 
            reuse=reuse, 
            **kwargs
        )

    def _predict_op(self, logits, **kwargs):
        return logits

    def _predict_proba_op(self, logits, **kwargs):
        return tf.no_op()