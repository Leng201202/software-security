"""Build a bounded S3 teaching policy; this does not contact AWS.
Use a bucket-level ListBucket statement conditioned on the prefix, plus an
object-level GetObject statement. Keep the original insecure/reference JSON.
"""
def build_policy(bucket, prefix):
    """Allow GetObject only under prefix, and ListBucket only for that prefix."""
    raise NotImplementedError("write the least-privilege policy")
