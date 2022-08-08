cudnn_benchmark = False
deterministic = True
seed = 1

# model setting
model = dict(
    type='MixFormer',
    backbone=dict(
        type='ConvolutionalVisionTransformer',
        spec=dict(
            NUM_STAGES=3,
            PATCH_SIZE=[7, 3, 3],
            PATCH_STRIDE=[4, 2, 2],
            PATCH_PADDING=[2, 1, 1],
            DIM_EMBED=[64, 192, 384],
            NUM_HEADS=[1, 3, 6],
            DEPTH=[1, 4, 16],
            MLP_RATIO=[4, 4, 4],
            ATTN_DROP_RATE=[0.0, 0.0, 0.0],
            DROP_RATE=[0.0, 0.0, 0.0],
            DROP_PATH_RATE=[0.0, 0.0, 0.1],
            QKV_BIAS=[True, True, True],
            CLS_TOKEN=[False, False, False],
            POS_EMBED=[False, False, False],
            QKV_PROJ_METHOD=['dw_bn', 'dw_bn', 'dw_bn'],
            KERNEL_QKV=[3, 3, 3],
            PADDING_KV=[1, 1, 1],
            STRIDE_KV=[2, 2, 2],
            PADDING_Q=[1, 1, 1],
            STRIDE_Q=[1, 1, 1],
            FREEZE_BN=True)),
    head=dict(
        type='MixFormerHead',
        bbox_head=dict(
            type='CornerPredictorHead',
            inplanes=384,
            channel=384,
            feat_size=20,
            stride=16),
        score_head=dict(
            type='MixFormerScoreDecoder',
            pool_size=4,
            feat_sz=20,
            stride=16,
            num_heads=6,
            hidden_dim=384,
            num_layers=3)),
    test_cfg=dict(
        search_factor=5.0,
        search_size=320,
        template_factor=2.0,
        template_size=128,
        update_interval=[10],
        online_size=[2],
        max_score_decay=[0.98],
    ))

data_root = 'data/'

img_norm_cfg = dict(mean=[0, 0, 0], std=[1, 1, 1], to_rgb=True)
test_pipeline = [
    dict(type='LoadImageFromFile', to_float32=True),
    dict(type='LoadAnnotations', with_bbox=True, with_label=False),
    dict(
        type='MultiScaleFlipAug',
        scale_factor=1,
        flip=False,
        transforms=[
            dict(type='Normalize', **img_norm_cfg),
            dict(type='VideoCollect', keys=['img', 'gt_bboxes']),
            dict(type='ImageToTensor', keys=['img'])
        ])
]
# dataset settings
data = dict(
    samples_per_gpu=16,
    workers_per_gpu=8,
    persistent_workers=True,
    samples_per_epoch=60000,
    test=dict(
        type='GOT10kDataset',
        ann_file=data_root + 'got10k/annotations/got10k_test_infos.txt',
        img_prefix=data_root + 'got10k',
        pipeline=test_pipeline,
        split='test',
        test_mode=True))

# yapf:enable
# runtime settings
total_epochs = 500
dist_params = dict(backend='nccl')
log_level = 'INFO'
work_dir = './work_dirs/xxx'
load_from = None
resume_from = None
workflow = [('train', 1)]
