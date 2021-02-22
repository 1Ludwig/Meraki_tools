import api_info
import meraki
from datetime import datetime

# Defining your API key as a variable in source code is not recommended
API_KEY = api_info.api_nyckel
# Instead, use an environment variable as shown under the Usage section
# @ https://github.com/meraki/dashboard-api-python/

dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)


serial_list = []


def findOrg(network_id_lookup):
    """ Fetch organisation ID's and put them in a dict """
    org_dict = dashboard.organizations.getOrganizations()

    """From the dict of organisations, make a list of networks associated with the organisation"""
    for org_list_loop in org_dict:
        try:
            """If a network doesn't have a License like a lab or test it gives API Error then just skip it"""
            network_dict = dashboard.organizations.getOrganizationNetworks(
                org_list_loop.get("id"), suppress_logging=True
            )
        except meraki.APIError:
            continue

        """From the list of Networks, find a network based matched on network_id_lookup"""
        for network_list_loop in network_dict:
            # print(network_list_loop.get("id"))
            if network_id_lookup == network_list_loop.get("id"):
                # print(network_lookup_id)
                org = str(org_list_loop.get("name"))
                network_name = str(network_list_loop.get("name"))
                return {"org_name": org, "net_name": network_name}


#
def main():
    for serial in serial_list:
        try:
            device_info = dashboard.devices.getDevice(serial)
            network_id = device_info.get("networkId")
            org_info = findOrg(network_id)
            print(
                f"""
Organisation: {org_info.get("org_name")}
Network: {org_info.get("net_name")}
Device Name: {device_info.get("name")}
Device Model: {device_info.get("model")}
Serial Number: {serial}
    """
            )
        except meraki.APIError:
            print(f"###\nFailed to get info from: {serial}\n###")


#

if __name__ == "__main__":
    start_time = datetime.now()
    main()
    print("\nElapsed time: " + str(datetime.now() - start_time))
