
# version 30001

data_pipeline_general

_rlnPipeLineJobCounter                      32
 

# version 30001

data_pipeline_processes

loop_ 
_rlnPipeLineProcessName #0 
_rlnPipeLineProcessAlias #1 
_rlnPipeLineProcessType #2 
_rlnPipeLineProcessStatus #3 
Import/job001/ Import/movies/            0            2 
MotionCorr/job002/ MotionCorr/relioncor2/            1            2 
CtfFind/job003/ CtfFind/ctffind4/            2            2 
ManualPick/job004/ ManualPick/justatest/            3            2 
Select/job005/ Select/5mics/            7            2 
AutoPick/job006/ AutoPick/LoG/            4            2 
Extract/job007/ Extract/LoG/            5            2 
Class2D/job008/ Class2D/LoG/            8            2 
Select/job009/ Select/templates4autopick/            7            2 
AutoPick/job010/ AutoPick/optimise_params/            4            2 
AutoPick/job011/ AutoPick/template/            4            2 
Extract/job012/ Extract/template/            5            2 
Class2D/job013/ Class2D/template/            8            2 
Select/job014/ Select/class2d_template/            7            2 
InitialModel/job015/ InitialModel/symC1/           18            2 
Class3D/job016/ Class3D/first_exhaustive/            9            2 
Select/job017/ Select/class3d_first_exhaustive/            7            2 
Extract/job018/ Extract/best3dclass_bigbox/            5            2 
Refine3D/job019/ Refine3D/first3dref/           10            2 
MaskCreate/job020/ MaskCreate/first3dref/           12            2 
PostProcess/job021/ PostProcess/first3dref/           15            2 
CtfRefine/job022/ CtfRefine/aberrations/           21            2 
CtfRefine/job023/ CtfRefine/magnification/           21            2 
CtfRefine/job024/ CtfRefine/defocus/           21            2 
Refine3D/job025/ Refine3D/ctfrefined/           10            2 
PostProcess/job026/ PostProcess/ctfrefined/           15            2 
Polish/job027/ Polish/train/           20            2 
Polish/job028/ Polish/polish/           20            2 
Refine3D/job029/ Refine3D/shiny/           10            2 
PostProcess/job030/ PostProcess/shiny/           15            2 
LocalRes/job031/ LocalRes/shiny/           16            2 
 

# version 30001

data_pipeline_nodes

loop_ 
_rlnPipeLineNodeName #0 
_rlnPipeLineNodeType #1 
Import/job001/movies.star            0 
MotionCorr/job002/corrected_micrographs.star            1 
MotionCorr/job002/logfile.pdf           13 
MotionCorr/job003/corrected_micrographs.star            1 
CtfFind/job003/micrographs_ctf.star            1 
CtfFind/job003/logfile.pdf           13 
ManualPick/job004/coords_suffix_manualpick.star            2 
ManualPick/job004/micrographs_selected.star            1 
Select/job005/micrographs_selected.star            1 
AutoPick/job006/coords_suffix_autopick.star            2 
AutoPick/job006/logfile.pdf           13 
Extract/job007/particles.star            3 
Extract/job008/particles.star            3 
Class2D/job008/run_it025_data.star            3 
Class2D/job008/run_it025_model.star            8 
Select/job009/particles.star            3 
Select/job009/class_averages.star            5 
AutoPick/job010/coords_suffix_autopick.star            2 
AutoPick/job010/logfile.pdf           13 
AutoPick/job011/coords_suffix_autopick.star            2 
AutoPick/job011/logfile.pdf           13 
Extract/job012/particles.star            3 
Class2D/job013/run_it025_data.star            3 
Class2D/job013/run_it025_model.star            8 
Select/job014/particles.star            3 
Select/job014/class_averages.star            5 
InitialModel/job015/run_it150_data.star            3 
InitialModel/job015/run_it150_model.star            8 
InitialModel/job015/run_it150_class001.mrc            6 
InitialModel/job015/run_it150_class001_symD2.mrc            6 
Class3D/job016/run_it025_data.star            3 
Class3D/job016/run_it025_model.star            8 
Class3D/job016/run_it025_class001.mrc            6 
Class3D/job016/run_it025_class002.mrc            6 
Class3D/job016/run_it025_class003.mrc            6 
Class3D/job016/run_it025_class004.mrc            6 
Select/job017/particles.star            3 
Extract/job018/particles.star            3 
Extract/job018/coords_suffix_extract.star            2 
Class3D/job016/run_it025_class001_box256.mrc            6 
Refine3D/job019/run_data.star            3 
Refine3D/job019/run_half1_class001_unfil.mrc           10 
Refine3D/job019/run_class001.mrc            6 
MaskCreate/job020/mask.mrc            7 
PostProcess/job021/postprocess.mrc           11 
PostProcess/job021/postprocess_masked.mrc           11 
PostProcess/job021/logfile.pdf           13 
PostProcess/job021/postprocess.star           14 
CtfRefine/job022/logfile.pdf           13 
CtfRefine/job022/particles_ctf_refine.star            3 
CtfRefine/job023/logfile.pdf           13 
CtfRefine/job023/particles_ctf_refine.star            3 
CtfRefine/job024/logfile.pdf           13 
CtfRefine/job024/particles_ctf_refine.star            3 
Refine3D/job025/run_data.star            3 
Refine3D/job025/run_half1_class001_unfil.mrc           10 
Refine3D/job025/run_class001.mrc            6 
PostProcess/job026/postprocess.mrc           11 
PostProcess/job026/postprocess_masked.mrc           11 
PostProcess/job026/logfile.pdf           13 
PostProcess/job026/postprocess.star           14 
Polish/job027/opt_params_all_groups.txt           15 
Polish/job028/logfile.pdf           13 
Polish/job028/shiny.star            3 
Refine3D/job029/run_data.star            3 
Refine3D/job029/run_half1_class001_unfil.mrc           10 
Refine3D/job029/run_class001.mrc            6 
PostProcess/job030/postprocess.mrc           11 
PostProcess/job030/postprocess_masked.mrc           11 
PostProcess/job030/logfile.pdf           13 
PostProcess/job030/postprocess.star           14 
LocalRes/job031/relion_locres_filtered.mrc           11 
LocalRes/job031/relion_locres.mrc           12 
LocalRes/job031/flowchart.pdf           13 
 

# version 30001

data_pipeline_input_edges

loop_ 
_rlnPipeLineEdgeFromNode #0 
_rlnPipeLineEdgeProcess #1 
Import/job001/movies.star MotionCorr/job002/ 
MotionCorr/job003/corrected_micrographs.star CtfFind/job003/ 
MotionCorr/job002/corrected_micrographs.star CtfFind/job003/ 
CtfFind/job003/micrographs_ctf.star ManualPick/job004/ 
ManualPick/job004/coords_suffix_manualpick.star Select/job005/ 
Select/job005/micrographs_selected.star AutoPick/job006/ 
CtfFind/job003/micrographs_ctf.star Extract/job007/ 
AutoPick/job006/coords_suffix_autopick.star Extract/job007/ 
Select/job005/micrographs_selected.star Extract/job007/ 
Extract/job008/particles.star Class2D/job008/ 
Extract/job007/particles.star Class2D/job008/ 
Class2D/job008/run_it025_model.star Select/job009/ 
Select/job005/micrographs_selected.star AutoPick/job010/ 
Select/job009/class_averages.star AutoPick/job010/ 
CtfFind/job003/micrographs_ctf.star AutoPick/job011/ 
Select/job009/class_averages.star AutoPick/job011/ 
Select/job005/micrographs_selected.star Extract/job012/ 
AutoPick/job011/coords_suffix_autopick.star Extract/job012/ 
CtfFind/job003/micrographs_ctf.star Extract/job012/ 
Extract/job012/particles.star Class2D/job013/ 
Class2D/job013/run_it025_model.star Select/job014/ 
Select/job014/particles.star InitialModel/job015/ 
Select/job014/particles.star Class3D/job016/ 
InitialModel/job015/run_it150_class001_symD2.mrc Class3D/job016/ 
Class3D/job016/run_it025_model.star Select/job017/ 
CtfFind/job003/micrographs_ctf.star Extract/job018/ 
Select/job017/particles.star Extract/job018/ 
Extract/job018/particles.star Refine3D/job019/ 
Class3D/job016/run_it025_class001_box256.mrc Refine3D/job019/ 
Refine3D/job019/run_class001.mrc MaskCreate/job020/ 
MaskCreate/job020/mask.mrc PostProcess/job021/ 
Refine3D/job019/run_half1_class001_unfil.mrc PostProcess/job021/ 
Refine3D/job019/run_data.star CtfRefine/job022/ 
Refine3D/job019/run_data.star CtfRefine/job023/ 
CtfRefine/job022/particles_ctf_refine.star CtfRefine/job023/ 
CtfRefine/job023/particles_ctf_refine.star CtfRefine/job024/ 
CtfRefine/job024/particles_ctf_refine.star Refine3D/job025/ 
Refine3D/job019/run_class001.mrc Refine3D/job025/ 
MaskCreate/job020/mask.mrc PostProcess/job026/ 
Refine3D/job025/run_half1_class001_unfil.mrc PostProcess/job026/ 
Refine3D/job025/run_data.star Polish/job027/ 
Refine3D/job025/run_data.star Polish/job028/ 
Polish/job028/shiny.star Refine3D/job029/ 
Refine3D/job025/run_class001.mrc Refine3D/job029/ 
MaskCreate/job020/mask.mrc Refine3D/job029/ 
MaskCreate/job020/mask.mrc PostProcess/job030/ 
Refine3D/job029/run_half1_class001_unfil.mrc PostProcess/job030/ 
Refine3D/job029/run_half1_class001_unfil.mrc LocalRes/job031/ 
 

# version 30001

data_pipeline_output_edges

loop_ 
_rlnPipeLineEdgeProcess #0 
_rlnPipeLineEdgeToNode #1 
Import/job001/ Import/job001/movies.star 
MotionCorr/job002/ MotionCorr/job002/corrected_micrographs.star 
MotionCorr/job002/ MotionCorr/job002/logfile.pdf 
CtfFind/job003/ CtfFind/job003/micrographs_ctf.star 
CtfFind/job003/ CtfFind/job003/logfile.pdf 
ManualPick/job004/ ManualPick/job004/coords_suffix_manualpick.star 
ManualPick/job004/ ManualPick/job004/micrographs_selected.star 
Select/job005/ Select/job005/micrographs_selected.star 
AutoPick/job006/ AutoPick/job006/coords_suffix_autopick.star 
AutoPick/job006/ AutoPick/job006/logfile.pdf 
Extract/job007/ Extract/job007/particles.star 
Class2D/job008/ Class2D/job008/run_it025_data.star 
Class2D/job008/ Class2D/job008/run_it025_model.star 
Select/job009/ Select/job009/particles.star 
Select/job009/ Select/job009/class_averages.star 
AutoPick/job010/ AutoPick/job010/coords_suffix_autopick.star 
AutoPick/job010/ AutoPick/job010/logfile.pdf 
AutoPick/job011/ AutoPick/job011/coords_suffix_autopick.star 
AutoPick/job011/ AutoPick/job011/logfile.pdf 
Extract/job012/ Extract/job012/particles.star 
Class2D/job013/ Class2D/job013/run_it025_data.star 
Class2D/job013/ Class2D/job013/run_it025_model.star 
Select/job014/ Select/job014/particles.star 
Select/job014/ Select/job014/class_averages.star 
InitialModel/job015/ InitialModel/job015/run_it150_data.star 
InitialModel/job015/ InitialModel/job015/run_it150_model.star 
InitialModel/job015/ InitialModel/job015/run_it150_class001.mrc 
InitialModel/job015/ InitialModel/job015/run_it150_class001_symD2.mrc 
Class3D/job016/ Class3D/job016/run_it025_data.star 
Class3D/job016/ Class3D/job016/run_it025_model.star 
Class3D/job016/ Class3D/job016/run_it025_class001.mrc 
Class3D/job016/ Class3D/job016/run_it025_class002.mrc 
Class3D/job016/ Class3D/job016/run_it025_class003.mrc 
Class3D/job016/ Class3D/job016/run_it025_class004.mrc 
Class3D/job016/ Class3D/job016/run_it025_class001_box256.mrc 
Select/job017/ Select/job017/particles.star 
Extract/job018/ Extract/job018/particles.star 
Extract/job018/ Extract/job018/coords_suffix_extract.star 
Refine3D/job019/ Refine3D/job019/run_data.star 
Refine3D/job019/ Refine3D/job019/run_half1_class001_unfil.mrc 
Refine3D/job019/ Refine3D/job019/run_class001.mrc 
MaskCreate/job020/ MaskCreate/job020/mask.mrc 
PostProcess/job021/ PostProcess/job021/postprocess.mrc 
PostProcess/job021/ PostProcess/job021/postprocess_masked.mrc 
PostProcess/job021/ PostProcess/job021/logfile.pdf 
PostProcess/job021/ PostProcess/job021/postprocess.star 
CtfRefine/job022/ CtfRefine/job022/logfile.pdf 
CtfRefine/job022/ CtfRefine/job022/particles_ctf_refine.star 
CtfRefine/job023/ CtfRefine/job023/logfile.pdf 
CtfRefine/job023/ CtfRefine/job023/particles_ctf_refine.star 
CtfRefine/job024/ CtfRefine/job024/logfile.pdf 
CtfRefine/job024/ CtfRefine/job024/particles_ctf_refine.star 
Refine3D/job025/ Refine3D/job025/run_data.star 
Refine3D/job025/ Refine3D/job025/run_half1_class001_unfil.mrc 
Refine3D/job025/ Refine3D/job025/run_class001.mrc 
PostProcess/job026/ PostProcess/job026/postprocess.mrc 
PostProcess/job026/ PostProcess/job026/postprocess_masked.mrc 
PostProcess/job026/ PostProcess/job026/logfile.pdf 
PostProcess/job026/ PostProcess/job026/postprocess.star 
Polish/job027/ Polish/job027/opt_params_all_groups.txt 
Polish/job028/ Polish/job028/logfile.pdf 
Polish/job028/ Polish/job028/shiny.star 
Refine3D/job029/ Refine3D/job029/run_data.star 
Refine3D/job029/ Refine3D/job029/run_half1_class001_unfil.mrc 
Refine3D/job029/ Refine3D/job029/run_class001.mrc 
PostProcess/job030/ PostProcess/job030/postprocess.mrc 
PostProcess/job030/ PostProcess/job030/postprocess_masked.mrc 
PostProcess/job030/ PostProcess/job030/logfile.pdf 
PostProcess/job030/ PostProcess/job030/postprocess.star 
LocalRes/job031/ LocalRes/job031/relion_locres_filtered.mrc 
LocalRes/job031/ LocalRes/job031/relion_locres.mrc 
LocalRes/job031/ LocalRes/job031/flowchart.pdf 
 
