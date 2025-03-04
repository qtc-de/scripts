#!/bin/bash

###############################################
#            Usage Information                #
###############################################
# This script can be used to setup a DHCP server
# powered by dnsmasq. To only provide DHCP, run
# the script with the desired interface as the
# first argument. If a second interface was
# specified, the script also enables forwarding
# from the first, to the second interface.
#
# Running this script flushes the custom-input
# and custom-forward local nft chains. Only use
# if changes to these chains are acceptable.

###############################################
#             Global Variables                #
###############################################
CONF="/tmp/dhcp-$(date +%s%N).conf"

###############################################
#           Function Definitions              #
###############################################
function enable_link()
{
    local INTERFACE

    echo "[+] Starting link setup."
    INTERFACE=$1

    sudo ip addr flush ${INTERFACE}
    sudo ip addr add 10.10.10.1/24 dev ${INTERFACE}
    sudo ip l set dev ${INTERFACE} up
}

function disable_link()
{
    local INTERFACE

    echo "[+] Starting link cleanup."
    INTERFACE=$1

    sudo ip addr flush ${INTERFACE}
    sudo ip l set dev ${INTERFACE} down
}

function enable_forwarding()
{
    local IF_FROM IF_TO

    IF_FROM=$1
    IF_TO=$2

    echo "[+] Starting firewall setup."
    sudo nft flush chain qubes custom-forward

    sudo nft add rule ip qubes custom-forward iifname "${IF_FROM}" oifname "${IF_TO}" accept
    sudo nft add rule ip qubes custom-forward ct state established,related accept

    sudo nft add chain ip qubes custom-postrouting \{ type nat hook postrouting priority 100 \; \}
    sudo nft add rule ip qubes custom-postrouting iifname "${IF_FROM}" oifname "${IF_TO}" masquerade

    sudo sysctl net.ipv4.ip_forward=1
}

function disable_forwarding()
{
    echo "[+] Starting firewall cleanup."
    sudo sysctl net.ipv4.ip_forward=0

    sudo nft flush chain qubes custom-forward
    sudo nft destroy chain qubes custom-postrouting
}

function enable_all()
{
    local IF_FROM IF_TO

    IF_FROM=$1
    IF_TO=$2

    enable_link ${IF_FROM}
    enable_forwarding ${IF_FROM} ${IF_TO}
    enable_dnsmasq ${IF_FROM} 53
}

function disable_all()
{
    local INTERFACE
    INTERFACE=$1

    disable_link ${INTERFACE}
    disable_forwarding
    disable_dnsmasq

    rm -f ${CONF}
}

function disable_dnsmasq()
{
    killall dnsmasq 2>/dev/null
    sudo nft flush chain qubes custom-input
}

function enable_dnsmasq()
{
    local INTERFACE DNS_PORT

    INTERFACE=$1
    DNS_PORT=$2

    cat <<EOF > ${CONF}
interface=${INTERFACE}
bind-interfaces

port=${DNS_PORT}
dhcp-range=10.10.10.1,10.10.10.5,1h
EOF

    echo "[+] Allowing incomming DHCP in firewall."
    sudo nft add rule ip qubes custom-input udp dport 67 accept

    if [ ${DNS_PORT} -gt 0 ]; then
        echo "[+] Allowing incomming DNS in firewall."
        sudo nft add rule ip qubes custom-input udp dport 53 accept
    fi

    set +e
    sudo dnsmasq --conf-file=${CONF} --no-daemon
}

###############################################
#              Main Script                    #
###############################################
set -e

if [ $# -lt 1 ]; then
    echo "$0 <INTF-IN> [<INTF-OUT>|clean]"
    exit 1
fi

if [ "$2" == "clean" ]; then
    disable_all $1
    exit 0
fi

trap "disable_all $1" SIGINT

if [ $# -eq 1 ]; then
    enable_link $1
    enable_dnsmasq $1 0

elif [ $# -eq 2 ]; then
    enable_all $1 $2
fi

disable_all $1
