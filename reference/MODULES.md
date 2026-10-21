# DeepInfer 模块表

| 编码 | 模块 | 定位 | 主要源码/产物 |
| --- | --- | --- | --- |
| M00 | 整体架构（overview） | DeepInfer 的目标、分层、请求主线与模块关系 | `docs/chapters/00-overview/`；上游 README；`entrypoints/`、`engine/`、`worker/`、`model_executor/`、`csrc/`、`deep_cluster/` |
| M01 | 前置理论（prereq-theory） | 理解 DeepInfer 的最小理论 | 前置章节；术语表 |
| M02 | 前置代码（prereq-code） | 读懂和改动 DeepInfer 的最小工程能力 | 前置教程；最小可运行示例 |
| M03 | 调度与执行（scheduling） | 请求从入口到执行的主线 | `entrypoints/`；`engine/`；`worker/`；`csrc/engine/` |
| M04 | 缓存与资源管理（cache） | KV cache 与显存/资源管理 | `worker/cache_engine.py`；`csrc/engine/block_manager.hpp`；tilelang cache ops；`shared_memory.py` |
| M05 | 模型结构（model） | DeepSeek 模型的结构、配置与权重加载 | `model_executor/models/`；`model_loader.py`；`model_metadata_utils.py`；`model_output.py`；`hugging_face/`；`layers/attention_backend.py`；`layers/linear.py`；`layers/layernorm.py`；`layers/rotary_embedding.py`；`layers/vocab_parallel_embedding.py` |
| M06 | 算子与内核（kernels） | 算子、kernel 与底层计算实现 | `model_executor/layers/tilelang_ops/`；`deepinfer/_C/`；`csrc/`；`npu_ops/`；`layers/sampler.py`；`fused_sample.py`；`fused_transform.py` |
| M07 | 多模态与视觉（multimodal） | 视觉编码与多模态输入 | `deepinfer/ve/`；`model_executor/models/vision_encoder/`；`models/deepseek_vl.py`；`multimodal_tokens.py`；`tilelang_ops/image_embed_ops.py`；`npu_ops/vit_attn.py` |
| M08 | 并行与通信（parallel） | 多卡/多机并行与通信 | `parallel_utils/`；`eplb/`；`distributed/`；`deep_cluster/`；`vendor/DeepEP` |
| M09 | 高级机制（advanced） | 解码与执行的高级策略 | `structure_output/`；dflash ops；`schedule_mtp_varlen`；`sampler.py`；`examples/_structured_output.py` |
| M10 | 验证与性能（eval） | 正确性、回归、基准与 profiling | `eval/`；`examples/benchmark.py`；`examples/sweep/`；`tests/`；`graph_timer` |
| M11 | 外置组件（external） | DeepInfer 依赖的外部算子/库最小闭包 | `vendor/`；各 vendor 上游仓库 |
| M12 | 工程与实践（platform） | 构建、平台、部署与模型适配 | `build.sh`；`scripts/`；`platform.py`；`deep_cluster/hardware/`；`topology/`；`examples/`；`requirements*.txt` |

