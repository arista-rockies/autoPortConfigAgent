# Arista Auto Port Config Agent
Spiritual successor to the work by https://github.com/jonathansm/arista-scripts.

This EOS agent will configure interfaces based on MAC, OUI, or LLDP connected to ports when they become operational.  Configuration data can be specified in either YAML or JSON format. Examples of both formats are provided in this repository.  Ports can also be configured to a default state when they transition to either the link down or link up states.

## Run Location and parameters
This python agent should be stored in /mnt/flash and is run using the EOS daemon syntax.  There are currently three configuration options

- "interfaces" an EOS configuration string representing the interfaces that you'd like to monitor.  This string should follow the same syntax as specifying a range in cli configuration mode.  Interface names will be resolved internally to their proper fully qualified forms.  For example: specifying "e1-4" will be automatically expanded as needed to include Ethernet1 through Ethernet4 inclusive.  The use of the keyword "all", or not setting an interfaces option at all, can be used to monitor all interfaces, however this should be used with caution as it may reconfigure uplink or management ports and disconnect the switch from the network!
- "config" can be, in preferred order, a single line json formatted string of configuration data, a file on the local switch filesystem, an http/https url to fetch a remote configuration file
- "vrf" is required when a) using a remote fetch and b) the switch cannot contact the server in the default vrf.  this option is ignored for the other two config variable options.
- "enableLLDP" defaults to True.  can be True or False. Determines if action on LLDP pdus is desired.  (the daemon will listen for and log LLDP pdus regardless as to this setting)

### Daemon configuration
Local access to api management interfaces must be configured for this agent to function properly.  This can be done with configuration similar to
```
management api http-commands
   protocol unix-socket
   no shutdown
   !
   vrf Management
      no shutdown
!
```

Configuration of the daemon is accomplished as follows

```
daemon portSet
   exec /mnt/flash/autoPortConfigAgent.py
   option interfaces value all
   option config value https://raw.githubusercontent.com/arista-rockies/autoPortConfigAgent/main/autoPortConfigAgent.json.example
   option vrf value Management
   no shutdown
!
```

### Detailed operation
This agent will parse the configuration for lists of specific mac addresses, oui addresses, or lldp attribute sets and monitor a set of interfaces for linkup and lindown events.

#### linkup event
Upon a linkup event for a monitored interface, the agent will begin watching for new mac addresses to be learned on that interface. When a mac address is learned the agent will,
1. Disable monitoring for that interface
2. Search the configuration for a mac, oui address, or lldp match
3. Apply matched specific mac configuration, or if there is no specific match, apply the matched oui confiugration to the interface.
4. Continue monitoring for link state change notifications

#### linkdown event
If an interface transitions to a linkdown state, a default configuration can be set on the interface.  If no default is specified in the configuration, no changes will be made.

#### lldp configuration options
The configuration also supports lldp options on the port.  The example configurations contain lldp configuration options.

#### Supported lldp attributes
Currently one can match on the lldp capabilities, the as substring search of the remote lldp agent description, the port mac address advertised in the lldppdu, or a combination of these.  When matching capabilities, the list of capabilities must match completely—subsets or supersets are not treated as a match.

### CVP warning
This script does not interface with CVP.  As such any configuration applied to the switch may cause the switch to show as out-of-sync within any CVP instance to which this switch is tied.  Manual reconciliation would be required.
