# Two unlocked 2080 Tis: NVLink / NCCL

Both Leadtek RTX 2080 Ti cards are physically VRAM-modded from 11 GB to 22 GB.
The local loader unlocks them sequentially. Pre-driver selector profiles were
0/0 and 0x6004/0. Both completed the firmware transaction and driver handoff.
Short FP16/FP32 instruction tests measured 110.5 and 114.3 TFLOPS; a 512x512
FP16 GEMM checked against FP64 passed on each. The local persistent combined
boot retains a 3090-only fallback. Public Turing source retains its original
single-target profile.

## NCCL check

Two-GPU float32 sum all-reduce through torch.cuda.nccl.all_reduce, PyTorch 2.8.0+cu129,
NCCL 2.27.3, NVIDIA 595.99.02. UUID-selected pair; topology NV2; peer access true
both ways; NCCL logged P2P/direct-pointer channels. Inputs 1 and 2; every output
element checked to equal 3. Five warmups and 20 timed calls per size, both GPUs
synchronized around the host timer. Times include Python launch overhead.

| Bytes per GPU | Mean ms | Algorithm GB/s | Output check |
|---:|---:|---:|---|
| 1024 | 0.018 | 0.057 | Passed |
| 1048576 | 0.059 | 17.690 | Passed |
| 16777216 | 0.497 | 33.790 | Passed |
| 67108864 | 1.825 | 36.770 | Passed |

This validates the current unlocked pair's short NCCL workflow with its NV2
connection. vLLM TP=2 and multi-hour communication testing are follow-up work.
