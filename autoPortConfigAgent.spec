%define _rpmfilename %%{NAME}-%%{VERSION}.%%{ARCH}.rpm

Name:           autoPortConfigAgent
Version:        2.5.2
Release:        1%{?dist}
Summary:        Automatically configure ports based on mac or lldp information
BuildArch:	noarch

License:        GPL
URL:            https://github.com/arista-rockies/autoPortConfigAgent
Source0:	https://github.com/arista-rockies/autoPortConfigAgent/archive/refs/tags/v%{version}.tar.gz

%description
Arista EOS Agent that will configure ports based on mac address or lldp information of the connected device


%prep
#%autosetup
%setup


%install
#%make_install
mkdir -p %{buildroot}/mnt/flash
install -m 600 autoPortConfigAgent.json.example %{buildroot}/mnt/flash/autoPortConfigAgent.json.example
install -m 600 autoPortConfigAgent.yml.example %{buildroot}/mnt/flash/autoPortConfigAgent.yml.example
install -m 755 autoPortConfigAgent.py %{buildroot}/mnt/flash/autoPortConfigAgent.py


%files
/mnt/flash/autoPortConfigAgent.py
/mnt/flash/autoPortConfigAgent.json.example
/mnt/flash/autoPortConfigAgent.yml.example


%changelog
* Wed Oct 19 2022 Patrick Felt <fatpelt@gmail.com>
- 
