import os, sys, argparse
from app import create_app

#################################################################
# Selecting the .env file to use for deployment (default = dev) #
#################################################################

selected_env_file = None

# Creating a dictionary of flask_app.py options (--config=dev) and their matching environment variables files aliases (dev)
possible_env_values = {
    "--config=local": "local",
    "--config=dev": "dev",
    "--config=prod": "prod",
    "--config=test": "test"
}
# Creating a flask_app.py --help listing these options
parser = argparse.ArgumentParser(
    description='Flask app for dico-topo'
)
parser.add_argument('--config=', type=str, default='dev', help="/".join([str(ele) for ele in possible_env_values.values()]) + ' to select the appropriate .env file to use, default=dev', metavar='')
args = parser.parse_args()

# Checking on the .env to be selected for deployment
# For server deployments, the .env name can be provided from the server configuration
if os.environ.get('SERVER_ENV_CONFIG'):
    print("Server provided an .env file : ", os.environ.get('SERVER_ENV_CONFIG'))
    selected_env_file = os.environ.get('SERVER_ENV_CONFIG')

# Otherwise, check if .env file to use is provided in command line (with '--config=' option)
elif next((element for element in sys.argv if element in possible_env_values.keys()), None):
    print("User provided a .env file in command : ", possible_env_values[next(element for element in sys.argv if element in possible_env_values.keys())])
    selected_env_file = possible_env_values[next(element for element in sys.argv if element in possible_env_values.keys())]

# Finally, if no .env file name is provided, default it to dev
else:
    selected_env_file = 'dev'

print("selected_env_file : ", selected_env_file)

###############################################
# Launching app with the selected environment #
###############################################

flask_app = create_app(config_name=selected_env_file)

if __name__ == "__main__":
    flask_app.run(debug=True, port=5003, host='0.0.0.0')