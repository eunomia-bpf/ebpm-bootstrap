# merge the existing json into one json
import json
import os

output_dir = "./.output/"
config_filename = "./config.json"
ebpf_program_data = os.path.join(output_dir, "ebpf_program.json")
ring_buffer_layout_data = os.path.join(output_dir, "event_layout.json")

global_data = {}

# load global config data
with open(config_filename) as f:
    global_data = json.load(f)

# load ebpf program data
with open(ebpf_program_data) as f:
    ebpf_data = json.load(f)
    global_data.update(ebpf_data)

# load the ring buffer export type info
# and add it to the ebpf program data map if RingBuffer is used
with open(ring_buffer_layout_data) as f:
    ring_buffer_data = json.load(f)
    maps_data = global_data["maps"]
    # FIX ME: we only support one RING_BUFFER or perf buffer
    for map in maps_data:
        if map["type"] == "BPF_MAP_TYPE_RINGBUF" or map["type"] == "BPF_MAP_TYPE_PERF_EVENT_ARRAY":
            if len(ring_buffer_data) == 0:
                print("WARN: the BPF_MAP_TYPE_RINGBUF export is not used in the ebpf program.")
            map["export_data_types"] = ring_buffer_data[0]

print(json.dumps(global_data))
