#!/bin/python

import os
import sys
import argparse
from urllib import parse



def main():
    parser = argparse.ArgumentParser(description="Opens a URL in mpv.")
    parser.add_argument("url", help="The URL to open")
    parser.add_argument("--count", type=str, help="Pass count on the command line")
    parser.add_argument("--qute-selected-text", type=str, help="Passed selected url title")
    parser.add_argument("--qute-url", type=str, help="Pass url")
    parser.add_argument("--random_socket", default=False , action="store_true", help="If passed then a random socket file will be used (i.e., each video will be sent to a different player)")
    args, unknown = parser.parse_known_args()

    url = os.environ["QUTE_URL"]
    url = sys.argv[1]
    
    socket_file = os.path.join(
        os.environ["QUTE_DATA_DIR"],
        "mpv/mpv_socket"
    )
    os.makedirs(os.path.dirname(socket_file), exist_ok=True)

    # If a count is given with the QUTE_COUNT environment variable
    if "QUTE_COUNT" in os.environ:
        print("COUNT = ", os.environ["QUTE_COUNT"])
        socket_file = f"{socket_file}{os.environ["QUTE_COUNT"]}"
    # If count is given on the command line then use that to determine the socket file used
    if args.count:
        print("COUNT = ", args.count)
        socket_file = f"{socket_file}{args.count}"
    # If not count is given and the random_socket is used then set the socket to random
    elif args.random_socket:
        from random import randint
        socket_file = f"{socket_file}{randint(1000, 9999)}"

    if os.path.exists(socket_file):
        print(f"Socket file exists!")

        # Try to send append-play notification to mpv ipc-socket
        try:
            command = f'''{{ "command": ["loadfile", "{url}", "append-play"] }}'''
            output = os.system(f"echo {command!r} | socat - {socket_file} | grep success")
            if output == 0:

                # If successful then show success notification
                if "QUTE_FIFO" in os.environ:
                    with open(os.environ["QUTE_FIFO"], "w") as f:
                        f.write(f"""message-info 'MPV ({socket_file.split("/")[-1]}): Appended to queue.'""")
                exit()
            else:
                print("Failed to append to queue.")
                os.remove(socket_file)  # Remove the dead socket file
        except SystemExit:
            exit()
        except:
            # Notification if append-play failed
            print("Failed to append to queue")
            os.remove(socket_file)  # Remove the dead socket file

    # Open mpv
    try:
        # Display message
        with open(os.environ["QUTE_FIFO"], "w") as f:
            f.write(f"""message-info 'MPV ({socket_file.split("/")[-1]}): New instance started.'""")

        mpv_command = [ "mpv", "--profile=720p", f"--input-ipc-server={socket_file}", "--wayland-app-id=notification-video-nofocus", url, "&>/dev/null"]
        os.system(" ".join(mpv_command) + "  & disown")
    except:
        # except Exception as e:
        print(f"Failed to open mpv:")


if __name__ == "__main__":
    main()
