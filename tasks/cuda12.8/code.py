import argparse
import torch


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        choices=["cpu", "gpu"],
        help="Choose device: cpu or gpu",
    )

    args = parser.parse_args()
    device = torch.device(args.device)

    print("PyTorch version:", torch.__version__)
    print("Using device:", device)

    # Create tensors on selected device
    a = torch.randn(4, 4, device=device)
    b = torch.randn(4, 4, device=device)

    print("\nTensor A:\n", a)
    print("\nTensor B:\n", b)

    # Matrix multiplication
    c = torch.matmul(a, b)
    print("\nA @ B:\n", c)

    # Simple verification
    print("\nSum:", c.sum().item())

    # GPU diagnostics
    print("\nCUDA available:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("GPU name:", torch.cuda.get_device_name(0))


if __name__ == "__main__":
    main()
