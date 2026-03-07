# Runtime hook — runs before any user code in the frozen EXE
# Pre-imports jaraco so pkg_resources doesn't crash on startup
try:
    import jaraco.text
    import jaraco.functools
    import jaraco.context
    import jaraco.classes
except ImportError:
    pass
