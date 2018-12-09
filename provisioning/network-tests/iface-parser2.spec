---
- name: parser meta data
  parser_metadata:
    version: 1.0
    command: show interface
    network_os: ios

- name: match sections
  pattern_match:
    regex: "^(\\S+) is up,"
    match_all: yes
    match_greedy: yes
  register: section

- name: match interface values
  pattern_group:
    - name: match name
      pattern_match:
        regex: "^(\\S+)"
        content: "{{ item }}"
      register: name

    - name: match hardware
      pattern_match:
        regex: "Hardware is (\\S+),"
        content: "{{ item }}"
      register: type

    - name: match mtu
      pattern_match:
        regex: "MTU (\\d+)"
        content: "{{ item }}"
      register: mtu

    - name: match description
      pattern_match:
        regex: "Description: (.*)"
        content: "{{ item }}"
      register: description

    - name: match vlan
      pattern_match:
        regex: "Encapsulation 802.1Q Virtual LAN, Vlan ID  (\\d+)"
        content: "{{ item }}"
      register: vlan

    - name: match network
      pattern_match:
        regex: "Internet address is (.*)"
        content: "{{ item }}"
      register: network
  loop: "{{ section }}"
  register: interfaces

- name: generate json data structure
  json_template:
    template:
      - key: interface
        object:
          - key: name
            value: "{{ item.name.matches.0 }}"
          - key: type
            value: "{{ item.type.matches.0 }}"
          - key: mtu
            value: "{{ item.mtu.matches.0 }}"
          - key: description
            value: "{{ item.description.matches.0|default('None') }}"
          - key: vlan
            value: "{{ item.vlan.matches.0|default('None') }}"
          - key: network
            value: "{{ item.network.matches.0|default('None') }}"
  loop: "{{ interfaces }}"
  export: yes
  register: interface_facts

# this didn't work because some interfaces dont have a entry
#- name: generate json data structure for interfaces with vlans
#  json_template:
#    template:
#      - key: "{{ item.name.matches.0 }}"
#        object:
#        - key: config
#          object:
#            - key: name
#              value: "{{ item.name.matches.0 }}"
#            - key: type
#              value: "{{ item.type.matches.0 }}"
#            - key: mtu
#              value: "{{ item.mtu.matches.0 }}"
#            - key: description
#              value: "{{ item.description.matches.0|default('None') }}"
#  when: "'Vlan' is in item.description.matches.0"
#  loop: "{{ interfaces }}"
#  export: yes
#  register: interface_vlan_facts
