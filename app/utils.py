"""Miscellaneous utility functions."""

import os


def load_env_vars(path):
    """Load environment variables from a file."""
    with open(path) as f:
        for line in f:
            if "=" in line:
                # Split the line into the variable name and value
                var, value = line.split("=")

                # Strip leading and trailing whitespace from the variable name and value
                var = var.strip()
                value = value.strip()

                if var and value:
                    # Set the environment variable
                    os.environ[var] = value
