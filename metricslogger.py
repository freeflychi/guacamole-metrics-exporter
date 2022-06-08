# Copyright (c) 2022 Cisco Systems, Inc. and its affiliates
# All rights reserved.

# The license notice is:
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

# setup logging
log_format = ('[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s')

# Define basic configuration
logging.basicConfig(
    # Define logging level
    level=logging.INFO,
    # Declare the object  created to format the log messages
    format=log_format,
    # Declare handlers
    handlers=[
        logging.StreamHandler()
    ])

logger = logging.getLogger(f"Guacamole metrics :")
