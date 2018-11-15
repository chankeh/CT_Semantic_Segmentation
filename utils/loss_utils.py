import tensorflow as tf
# import tensorlayer as tl


def cross_entropy(y, logits, n_class):
    flat_logits = tf.reshape(logits, [-1, n_class])
    flat_labels = tf.reshape(y, [-1, n_class])
    try:
        loss = tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits_v2(
                logits=flat_logits, labels=flat_labels))
    except:
        loss = tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits(
                logits=flat_logits, labels=flat_labels))
    return loss


def dice_coeff(y, logits):
    # eps = 1e-5
    # prediction = pixel_wise_softmax(logits)
    # intersection = tf.reduce_sum(prediction * y)
    # union = eps + tf.reduce_sum(prediction) + tf.reduce_sum(y)
    # dice_loss = 1 - (2 * intersection / union)
    outputs = tl.act.pixel_wise_softmax(logits)
    dice_loss = 1 - tl.cost.dice_coe(outputs, y, loss_type='jaccard', axis=(1, 2, 3, 4))
    return dice_loss


def pixel_wise_softmax(output_map):
    num_classes = output_map.get_shape().as_list()[-1]
    exponential_map = tf.exp(output_map)
    try:
        sum_exp = tf.reduce_sum(exponential_map, 4, keepdims=True)
    except:
        sum_exp = tf.reduce_sum(exponential_map, 4, keep_dims=True)
    # tensor_sum_exp = tf.tile(sum_exp, tf.stack([1, 1, 1, tf.shape(output_map)[3]]))
    tensor_sum_exp = tf.tile(sum_exp, (1, 1, 1, 1, num_classes))
    return tf.div(exponential_map, tensor_sum_exp)


def weighted_cross_entropy(y, logits, n_class):
    flat_logits = tf.reshape(logits, [-1, n_class])
    flat_labels = tf.reshape(y, [-1, n_class])
    # your class weights
    class_weights = tf.constant([[1.0, 2.0, 10.0, 10.0, 2.0, 10.0]])
    # deduce weights for batch samples based on their true label
    weights = tf.reduce_sum(class_weights * flat_labels, axis=1)
    # compute your (unweighted) softmax cross entropy loss
    try:
        unweighted_losses = tf.nn.softmax_cross_entropy_with_logits_v2(labels=flat_labels, logits=flat_logits)
    except:
        unweighted_losses = tf.nn.softmax_cross_entropy_with_logits(labels=flat_labels, logits=flat_logits)

    # apply the weights, relying on broadcasting of the multiplication
    weighted_losses = unweighted_losses * weights
    # reduce the result to get your final loss
    loss = tf.reduce_mean(weighted_losses)
    return loss


