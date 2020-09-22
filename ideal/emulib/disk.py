import os
import json
from itertools import zip_longest

from command import sudo_commandex

mbr_int_to_name = {
    "1": "EFI System",
    "2": "MBR partition scheme",
    "3": "Intel Fast Flash",
    "4": "BIOS boot",
    "5": "Sony boot partition",
    "6": "Lenovo boot partition",
    "7": "PowerPC PReP boot",
    "8": "ONIE boot",
    "9": "ONIE config",
    "10": "Microsoft reserved",
    "11": "Microsoft basic data",
    "12": "Microsoft LDM metadata",
    "13": "Microsoft LDM data",
    "14": "Windows recovery environment",
    "15": "IBM General Parallel Fs",
    "16": "Microsoft Storage Spaces",
    "17": "HP-UX data",
    "18": "HP-UX service",
    "19": "Linux swap",
    "20": "Linux filesystem",
    "21": "Linux server data",
    "22": "Linux root (x86)",
    "23": "Linux root (ARM)",
    "24": "Linux root (x86-64)",
    "25": "Linux root (ARM-64)",
    "26": "Linux root (IA-64)",
    "27": "Linux reserved",
    "28": "Linux home",
    "29": "Linux RAID",
    "30": "Linux extended boot",
    "31": "Linux LVM",
    "32": "FreeBSD data",
    "33": "FreeBSD boot",
    "34": "FreeBSD swap",
    "35": "FreeBSD UFS",
    "36": "FreeBSD ZFS",
    "37": "FreeBSD Vinum",
    "38": "Apple HFS/HFS+",
    "39": "Apple UFS",
    "40": "Apple RAID",
    "41": "Apple RAID offline",
    "42": "Apple boot",
    "43": "Apple label",
    "44": "Apple TV recovery",
    "45": "Apple Core storage",
    "46": "Solaris boot",
    "47": "Solaris root",
    "48": "Solaris /usr & Apple ZFS",
    "49": "Solaris swap",
    "50": "Solaris backup",
    "51": "Solaris /var",
    "52": "Solaris /home",
    "53": "Solaris alternate sector",
    "54": "Solaris reserved 1",
    "55": "Solaris reserved 2",
    "56": "Solaris reserved 3",
    "57": "Solaris reserved 4",
    "58": "Solaris reserved 5",
    "59": "NetBSD swap",
    "60": "NetBSD FFS",
    "61": "NetBSD LFS",
    "62": "NetBSD concatenated",
    "63": "NetBSD encrypted",
    "64": "NetBSD RAID",
    "65": "ChromeOS kernel",
    "66": "ChromeOS root fs",
    "67": "ChromeOS reserved",
    "68": "MidnightBSD data",
    "69": "MidnightBSD boot",
    "70": "MidnightBSD swap",
    "71": "MidnightBSD UFS",
    "72": "MidnightBSD ZFS",
    "73": "MidnightBSD Vinum",
    "74": "Ceph Journal",
    "75": "Ceph Encrypted Journal",
    "76": "Ceph OSD",
    "77": "Ceph crypt OSD",
    "78": "Ceph disk in creation",
    "79": "Ceph crypt disk in creation",
    "80": "VMware VMFS",
    "81": "VMware Diagnostic",
    "82": "VMware Virtual SAN",
    "83": "VMware Virsto",
    "84": "VMware Reserved",
    "85": "OpenBSD data",
    "86": "QNX6 file system",
    "87": "Plan 9 partition",
}

name_to_mbr_int = {v: k for k, v in mbr_int_to_name.items()}

gpt_uuid_to_name = {
    "C12A7328-F81F-11D2-BA4B-00A0C93EC93B": "EFI System",
    "024DEE41-33E7-11D3-9D69-0008C781F39F": "MBR partition scheme",
    "D3BFE2DE-3DAF-11DF-BA40-E3A556D89593": "Intel Fast Flash",
    "21686148-6449-6E6F-744E-656564454649": "BIOS boot",
    "F4019732-066E-4E12-8273-346C5641494F": "Sony boot partition",
    "BFBFAFE7-A34F-448A-9A5B-6213EB736C22": "Lenovo boot partition",
    "9E1A2D38-C612-4316-AA26-8B49521E5A8B": "PowerPC PReP boot",
    "7412F7D5-A156-4B13-81DC-867174929325": "ONIE boot",
    "D4E6E2CD-4469-46F3-B5CB-1BFF57AFC149": "ONIE config",
    "E3C9E316-0B5C-4DB8-817D-F92DF00215AE": "Microsoft reserved",
    "EBD0A0A2-B9E5-4433-87C0-68B6B72699C7": "Microsoft basic data",
    "5808C8AA-7E8F-42E0-85D2-E1E90434CFB3": "Microsoft LDM metadata",
    "AF9B60A0-1431-4F62-BC68-3311714A69AD": "Microsoft LDM data",
    "DE94BBA4-06D1-4D40-A16A-BFD50179D6AC": "Windows recovery environment",
    "37AFFC90-EF7D-4E96-91C3-2D7AE055B174": "IBM General Parallel Fs",
    "E75CAF8F-F680-4CEE-AFA3-B001E56EFC2D": "Microsoft Storage Spaces",
    "75894C1E-3AEB-11D3-B7C1-7B03A0000000": "HP-UX data",
    "E2A1E728-32E3-11D6-A682-7B03A0000000": "HP-UX service",
    "0657FD6D-A4AB-43C4-84E5-0933C84B4F4F": "Linux swap",
    "0FC63DAF-8483-4772-8E79-3D69D8477DE4": "Linux filesystem",
    "3B8F8425-20E0-4F3B-907F-1A25A76F98E8": "Linux server data",
    "44479540-F297-41B2-9AF7-D131D5F0458A": "Linux root (x86)",
    "69DAD710-2CE4-4E3C-B16C-21A1D49ABED3": "Linux root (ARM)",
    "4F68BCE3-E8CD-4DB1-96E7-FBCAF984B709": "Linux root (x86-64)",
    "B921B045-1DF0-41C3-AF44-4C6F280D3FAE": "Linux root (ARM-64)",
    "993D8D3D-F80E-4225-855A-9DAF8ED7EA97": "Linux root (IA-64)",
    "8DA63339-0007-60C0-C436-083AC8230908": "Linux reserved",
    "933AC7E1-2EB4-4F13-B844-0E14E2AEF915": "Linux home",
    "A19D880F-05FC-4D3B-A006-743F0F84911E": "Linux RAID",
    "BC13C2FF-59E6-4262-A352-B275FD6F7172": "Linux extended boot",
    "E6D6D379-F507-44C2-A23C-238F2A3DF928": "Linux LVM",
    "516E7CB4-6ECF-11D6-8FF8-00022D09712B": "FreeBSD data",
    "83BD6B9D-7F41-11DC-BE0B-001560B84F0F": "FreeBSD boot",
    "516E7CB5-6ECF-11D6-8FF8-00022D09712B": "FreeBSD swap",
    "516E7CB6-6ECF-11D6-8FF8-00022D09712B": "FreeBSD UFS",
    "516E7CBA-6ECF-11D6-8FF8-00022D09712B": "FreeBSD ZFS",
    "516E7CB8-6ECF-11D6-8FF8-00022D09712B": "FreeBSD Vinum",
    "48465300-0000-11AA-AA11-00306543ECAC": "Apple HFS/HFS+",
    "55465300-0000-11AA-AA11-00306543ECAC": "Apple UFS",
    "52414944-0000-11AA-AA11-00306543ECAC": "Apple RAID",
    "52414944-5F4F-11AA-AA11-00306543ECAC": "Apple RAID offline",
    "426F6F74-0000-11AA-AA11-00306543ECAC": "Apple boot",
    "4C616265-6C00-11AA-AA11-00306543ECAC": "Apple label",
    "5265636F-7665-11AA-AA11-00306543ECAC": "Apple TV recovery",
    "53746F72-6167-11AA-AA11-00306543ECAC": "Apple Core storage",
    "6A82CB45-1DD2-11B2-99A6-080020736631": "Solaris boot",
    "6A85CF4D-1DD2-11B2-99A6-080020736631": "Solaris root",
    "6A898CC3-1DD2-11B2-99A6-080020736631": "Solaris /usr & Apple ZFS",
    "6A87C46F-1DD2-11B2-99A6-080020736631": "Solaris swap",
    "6A8B642B-1DD2-11B2-99A6-080020736631": "Solaris backup",
    "6A8EF2E9-1DD2-11B2-99A6-080020736631": "Solaris /var",
    "6A90BA39-1DD2-11B2-99A6-080020736631": "Solaris /home",
    "6A9283A5-1DD2-11B2-99A6-080020736631": "Solaris alternate sector",
    "6A945A3B-1DD2-11B2-99A6-080020736631": "Solaris reserved 1",
    "6A9630D1-1DD2-11B2-99A6-080020736631": "Solaris reserved 2",
    "6A980767-1DD2-11B2-99A6-080020736631": "Solaris reserved 3",
    "6A96237F-1DD2-11B2-99A6-080020736631": "Solaris reserved 4",
    "6A8D2AC7-1DD2-11B2-99A6-080020736631": "Solaris reserved 5",
    "49F48D32-B10E-11DC-B99B-0019D1879648": "NetBSD swap",
    "49F48D5A-B10E-11DC-B99B-0019D1879648": "NetBSD FFS",
    "49F48D82-B10E-11DC-B99B-0019D1879648": "NetBSD LFS",
    "2DB519C4-B10E-11DC-B99B-0019D1879648": "NetBSD concatenated",
    "2DB519EC-B10E-11DC-B99B-0019D1879648": "NetBSD encrypted",
    "49F48DAA-B10E-11DC-B99B-0019D1879648": "NetBSD RAID",
    "FE3A2A5D-4F32-41A7-B725-ACCC3285A309": "ChromeOS kernel",
    "3CB8E202-3B7E-47DD-8A3C-7FF2A13CFCEC": "ChromeOS root fs",
    "2E0A753D-9E48-43B0-8337-B15192CB1B5E": "ChromeOS reserved",
    "85D5E45A-237C-11E1-B4B3-E89A8F7FC3A7": "MidnightBSD data",
    "85D5E45E-237C-11E1-B4B3-E89A8F7FC3A7": "MidnightBSD boot",
    "85D5E45B-237C-11E1-B4B3-E89A8F7FC3A7": "MidnightBSD swap",
    "0394EF8B-237E-11E1-B4B3-E89A8F7FC3A7": "MidnightBSD UFS",
    "85D5E45D-237C-11E1-B4B3-E89A8F7FC3A7": "MidnightBSD ZFS",
    "85D5E45C-237C-11E1-B4B3-E89A8F7FC3A7": "MidnightBSD Vinum",
    "45B0969E-9B03-4F30-B4C6-B4B80CEFF106": "Ceph Journal",
    "45B0969E-9B03-4F30-B4C6-5EC00CEFF106": "Ceph Encrypted Journal",
    "4FBD7E29-9D25-41B8-AFD0-062C0CEFF05D": "Ceph OSD",
    "4FBD7E29-9D25-41B8-AFD0-5EC00CEFF05D": "Ceph crypt OSD",
    "89C57F98-2FE5-4DC0-89C1-F3AD0CEFF2BE": "Ceph disk in creation",
    "89C57F98-2FE5-4DC0-89C1-5EC00CEFF2BE": "Ceph crypt disk in creation",
    "AA31E02A-400F-11DB-9590-000C2911D1B8": "VMware VMFS",
    "9D275380-40AD-11DB-BF97-000C2911D1B8": "VMware Diagnostic",
    "381CFCCC-7288-11E0-92EE-000C2911D0B2": "VMware Virtual SAN",
    "77719A0C-A4A0-11E3-A47E-000C29745A24": "VMware Virsto",
    "9198EFFC-31C0-11DB-8F78-000C2911D1B8": "VMware Reserved",
    "824CC7A0-36A8-11E3-890A-952519AD3F61": "OpenBSD data",
    "CEF5A9AD-73BC-4601-89F3-CDEEEEE321A1": "QNX6 file system",
    "C91818F9-8025-47AF-89D2-F030D7000C2C": "Plan 9 partition",
}


name_to_gpt_uuid = {v: k for k, v in gpt_uuid_to_name.items()}


def sector_to_h(sectors):

    num_bytes = sectors * 512

    units = {'kb': 1, 'mb': 2, 'gb': 3, 'tb': 4}

    prev_val = 0
    prev_unit = "b"

    for unit, exp in units:
        val = num_bytes / (1024 ** exp)
        if val < 1:
            return f"{prev_val}{prev_unit}"
        prev_val = val
        prev_unit = unit


def h_to_sector(h_string):
    units = {'kb': 1, 'mb': 2, 'gb': 3, 'tb': 4}
    h_string = h_string.lower()

    unit = h_string[-2:]
    if unit not in units.keys():
        raise ValueError(f"Invalid unit: {unit}")
    val = float(h_string[0:-2])

    return val * (1024 ** units[unit]) / 512


class InvalidDevice(Exception):
    def __init__(self, path, error=None):
        self.path = path
        self.error = error

    def __str__(self):
        return f"InvalidDevice: {self.path}: {self.error}"


class Partition(object):
    device_path = None
    fs_type = None
    uuid = None

    def __init__(
        self,
        disk_path=None,
        num=None,
        device_path=None,
        fs_type=None,
        size=None,
        uuid=None,
    ):
        if device_path is not None:
            self.device_path = device_path
        elif disk_path is not None and num is not None:
            self.device_path = f"{disk_path}{num}"
        if fs_type is not None:
            self.fs_type = fs_type
        if size is not None:
            self.size = size
        if uuid is not None:
            self.uuid = uuid

    @property
    def size_sectors(self, val):


    def to_dict(self):
        return {
            "device_path": self.device_path,
            "fs_type": self.fs_type,
            "size": self.size,
            "uuid": self.uuid,
        }

    def __str__(self):
        return f"{self.device_path} {self.fs_type} {self.size} {self.uuid}"

    def __eq__(self, o):
        if self.device_path != o.device_path:
            return False
        if self.fs_type != o.fs_type:
            return False
        if self.size != o.size:
            return False
        # if one or more is missing a uuid don't count this as
        # inequality
        if self.uuid is not None and o.uuid is not None and self.uuid != o.uuid:
            return False
        return True


class Disk(object):
    """
    Represent a disk device
    """

    device_path = None
    label = None
    label_id = None
    unit = None
    partitions = None

    def __init__(self, device_name):
        if device_name.startswith("/dev/"):
            self.device_path = device_name
        else:
            self.device_path = os.path.join("/dev", device_name)

        if not os.path.exists(self.device_path):
            raise InvalidDevice(self.device_path, "Does not exist")
        if not os.access(self.device_path, os.W_OK):
            raise InvalidDevice(self.device_path, "Not writable")
        self.partitions = []

    def get_info(self):
        cmd = sudo_commandex("sfdisk", "-J", self.device_path)
        out = cmd.stdout

        # no label on the disk
        if b"does not contain a recognized partition table" in out:
            return

        disk_info = json.loads(out)

        self.label = disk_info["partitiontable"]["label"]
        self.label_id = disk_info["partitiontable"]["id"]
        self.unit = disk_info["partitiontable"]["unit"]

        for partition in disk_info["partitiontable"]["partitions"]:
            if self.label == "gpt":
                fs_type = gpt_uuid_to_name[partition["type"]]
            elif self.label == "mbr":
                fs_type = mbr_int_to_name[partition["type"]]
            else:
                fs_type = "invalid label"
            self.partitions.append(
                Partition(
                    device_path=partition["node"],
                    size=partition["size"],
                    fs_type=fs_type,
                    uuid=partition.get("uuid"),
                )
            )

    def to_dict(self):
        out = {
            "device_path": self.device_path,
            "label": self.label,
            "label_id": self.label_id,
            "unit": self.unit,
            "partitions": [],
        }
        for partition in self.partitions:
            out["partitions"].append(partition.to_dict())
        return out

    def to_json(self):
        return json.dumps(self.to_dict())

    def add_partition(self, partition):
        self.partitions.append(partition)

    def delta(self, new):
        if self.label != new.label:
            return "Entire disk will be overwritten"

        for i, parts in enumerate(zip_longest(self.partitions, new.partitions)):
            # If we're just tacking on more partitions
            if parts[0] is None:
                msg = "The following partitions will be added:\n"
                for part in new.partitions[i:]:
                    msg += f"{part}\n"
                return msg
            # If we're just deleting old partitions
            if parts[1] is None:
                msg = "The following partitions will be destroyed:\n"
                for part in self.partitions[i:]:
                    msg += f"{part}\n"
                return msg
            # If we're changing existing partitions, everything from the
            # first changed one will be destroyed
            if parts[0] != parts[1]:
                msg = "The following partitions will be overwritten:\n"
                for part in self.partitions[i:]:
                    msg += f"{part}\n"
                return msg


if __name__ == "__main__":
    mydisk = Disk("/dev/sda")
    mydisk.get_info()
    print("\nSDA info")
    print(mydisk.to_json())
    mydisk = Disk("/dev/sdb")
    mydisk.get_info()
    print("\nSDB info")
    print(mydisk.to_json())

    print("\nINVALID DISK")
    try:
        my_bad_disk = Disk("/dev/sdg")
    except InvalidDevice as e:
        print("Successfully invalid")
        print(e)

    print("\nCHANGE LABEL")
    fake_new_disk = Disk("/dev/sdb")
    fake_new_disk.label = "mbr"
    msg = mydisk.delta(fake_new_disk)
    print(msg)
    assert "Entire" in msg

    print("\nDELETE LAST PARTITION")
    fake_new_disk.label = mydisk.label
    fake_new_disk.partitions = mydisk.partitions[:-1]
    msg = mydisk.delta(fake_new_disk)
    print(msg)
    assert "destroyed" in msg
