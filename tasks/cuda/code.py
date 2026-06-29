#!/usr/bin/env python3

import sys
import time
import argparse
import torch


def fail(msg):
    print(f"❌ FAIL: {msg}")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="CUDA + PyTorch Validation")

    # ONLY NEW INPUTS
    parser.add_argument("--a-val", type=float, default=1.0,
                        help="Fill value for tensor A")

    parser.add_argument("--b-val", type=float, default=1.0,
                        help="Fill value for tensor B")

    args = parser.parse_args()

    print("=" * 60)
    print("CUDA + PyTorch Validation")
    print("=" * 60)

    print(f"Python: {sys.version.split()[0]}")
    print(f"PyTorch: {torch.__version__}")

    print(f"PyTorch CUDA version: {torch.version.cuda}")
    if torch.version.cuda is None:
        fail("PyTorch was not built with CUDA support.")

    if not torch.cuda.is_available():
        fail("CUDA is not available.")

    device_count = torch.cuda.device_count()
    print(f"CUDA devices: {device_count}")

    if device_count == 0:
        fail("No CUDA devices found.")

    for i in range(device_count):
        print(f"\nGPU {i}")
        print(f"  Name: {torch.cuda.get_device_name(i)}")
        maj, min = torch.cuda.get_device_capability(i)
        print(f"  Capability: {maj}.{min}")

    device = torch.device("cuda:0")

    print("\nRunning GPU computation...")

    # FIXED VALUES (no CLI control)
    N = 256

    torch.cuda.synchronize()
    start = time.perf_counter()

    # ONLY CHANGE: initialization uses CLI values
    a = torch.full((N, N), args.a_val, device=device)
    b = torch.full((N, N), args.b_val, device=device)

    c = torch.matmul(a, b)

    torch.cuda.synchronize()
    elapsed = time.perf_counter() - start

    print(f"Matrix multiply ({N}x{N}) completed in {elapsed:.3f}s")

    if not torch.isfinite(c).all():
        fail("Computation produced non-finite values.")

    checksum = c.sum().item()
    print(f"Checksum: {checksum:.6f}")

    allocated = torch.cuda.memory_allocated(device) / 1024**2
    reserved = torch.cuda.memory_reserved(device) / 1024**2

    print(f"Memory allocated: {allocated:.1f} MB")
    print(f"Memory reserved : {reserved:.1f} MB")

    del a, b, c
    torch.cuda.empty_cache()

    print("\n✅ SUCCESS")
    print("CUDA runtime is available.")
    print("PyTorch CUDA build is correct.")
    print("GPU computation completed successfully.")
    print("Memory allocation and synchronization succeeded.")


if __name__ == "__main__":
    main()
