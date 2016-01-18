#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess, os, sys
import zmq

MUSCLE_ADDR_PREFIX = '/alfred/muscle/'


def main(cli_args):
    spine_input, spine_output = init_io(cli_args)

    try:
        while True:
            try:
                message = spine_output.recv_string(flags=zmq.NOBLOCK)
                spine_input.send_string('/alfred/cli-output/muscle received ' + message)
            except zmq.Again:
                pass
    except KeyboardInterrupt:
        pass
        print "\n"


def init_io(cli_args):
    input_socket_addr = get_arg_by_index_or_default_env(cli_args, 1, 'ALFRED_SPINE_INPUT')
    spine_input = zmq.Context().socket(zmq.PUSH)
    spine_input.connect(input_socket_addr)

    output_socket_addr = get_arg_by_index_or_default_env(cli_args, 2, 'ALFRED_SPINE_OUTPUT')
    spine_output = zmq.Context().socket(zmq.SUB)
    spine_output.setsockopt(zmq.SUBSCRIBE, MUSCLE_ADDR_PREFIX)
    spine_output.connect(output_socket_addr)

    return spine_input, spine_output


def get_arg_by_index_or_default_env(cli_args, arg_index, env_key):
    if len(cli_args) > arg_index:
        return cli_args[arg_index]
    else:
        try:
            os.environ[env_key]
        except KeyError:
            sys.exit("Could not find Alfred's input socket from cli nor env var " + env_key)


if __name__ == '__main__':
    main(sys.argv)
