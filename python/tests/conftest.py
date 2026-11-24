from hypothesis import settings

settings.register_profile("reproducible", derandomize=True, max_examples=300, deadline=None)
settings.load_profile("reproducible")
