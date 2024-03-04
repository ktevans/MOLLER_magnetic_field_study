// Run using the following commands:
//  >> root -l
//  >> .L scripts/SlimGeneral.C
//  >> SlimGeneral("/path/to/input/file") 
//
// Do not include ".root" at the end of your input file.
// This will output a slimmed down file with the same name as the input file but ending in "_slim"
//
// The slimmed file will include primary electrons on the main detector (28), sieve virtual plane (270), and GEM detectors (32-35).
// The dataframe of the output is filtered to only include "good events" which are primary electrons that make it to the main detector.
// The target variables are made using the tree branch "part" which looks at where particles are generated from.
// After slimming the root file, the output file will include the following variables:
// "sieve_r", "sieve_ph", "main_r", "main_ph", "main_trid", "main_x", "main_y", "main_px", "main_py", "main_pz", "rate" , 
// "gem1_r", "gem1_ph", "sieve_ph", "sieve_px", "sieve_py", "sieve_pz", "gem1_x", "gem1_y", "gem4_x", "gem4_y",
// "gem1_px", "gem1_py", "gem1_pz", "sieve_x", "sieve_y", "tg_th", "tg_ph", "tg_p", "tg_vz"


void SlimGeneral(TString infile)
{
   auto fileName = Form("%s.root",infile.Data());
   auto outFileName = Form("%s_slim.root",infile.Data());
   auto treeName = "T";
   ROOT::RDataFrame d(treeName, fileName);

   auto primary_hit = "hit.pid==11 && hit.mtrid==0 && hit.trid==1";
   auto selected_df = d.Define("prm_e",primary_hit).Define("main","hit.det==28").Define("good_ev","Sum(prm_e && main)").Filter("good_ev>0");

   auto df_small = selected_df.Define("main_trid","hit.trid[main && prm_e][0]").Define("main_r","hit.r[main && prm_e && hit.trid==main_trid][0]")
          .Define("main_ph","hit.ph[main && prm_e && hit.trid==main_trid][0]")
          .Define("main_x","hit.x[main && prm_e && hit.trid==main_trid][0]").Define("main_y","hit.y[main && prm_e && hit.trid==main_trid][0]")
	  .Define("main_px","hit.px[ prm_e && main && hit.trid==main_trid][0]").Define("main_py","hit.py[ prm_e && main && hit.trid==main_trid][0]")
	  .Define("main_pz","hit.pz[ prm_e && main && hit.trid==main_trid][0]")
          .Define("sieve_trid","hit.trid[hit.det==270 && prm_e && hit.trid==main_trid][0]")
          .Define("sieve_r","hit.r[hit.det==270 && prm_e && hit.trid==main_trid][0]").Define("sieve_ph","hit.ph[hit.det==270 && prm_e && hit.trid==main_trid][0]")
          .Define("sieve_x","hit.x[hit.det==270 && prm_e && hit.trid==main_trid][0]").Define("sieve_y","hit.y[hit.det==270 && prm_e && hit.trid==main_trid][0]")
          .Define("sieve_z","hit.z[hit.det==270 && prm_e && hit.trid==main_trid][0]").Define("sieve_px","hit.px[hit.det==270 && prm_e && hit.trid==main_trid][0]")
          .Define("sieve_py","hit.py[hit.det==270 && prm_e && hit.trid==main_trid][0]").Define("sieve_pz","hit.pz[hit.det==270 && prm_e && hit.trid==main_trid][0]")
	  .Define("gem1_trid","hit.trid[ prm_e && hit.det==32 && hit.trid==main_trid][0]")
          .Define("gem1_r","hit.r[ prm_e && hit.det==32 && hit.trid==main_trid][0]").Define("gem1_ph","hit.ph[ prm_e && hit.det==32 && hit.trid==main_trid][0]")
	  .Define("gem1_x","hit.x[ prm_e && hit.det==32 && hit.trid==main_trid][0]").Define("gem1_y","hit.y[prm_e && hit.det==32 && hit.trid==main_trid][0]")
	  .Define("gem1_px","hit.px[ prm_e && hit.det==32 && hit.trid==main_trid][0]").Define("gem1_py","hit.py[ prm_e && hit.det==32 && hit.trid==main_trid][0]")
	  .Define("gem1_pz","hit.pz[ prm_e && hit.det==32 && hit.trid==main_trid][0]").Define("gem1_k","hit.k[ prm_e && hit.det==32 && hit.trid==main_trid][0]")
          .Define("gem1_vx","hit.vx[ prm_e && hit.det==32 && hit.trid==main_trid][0]").Define("gem1_vy","hit.vy[ prm_e && hit.det==32 && hit.trid==main_trid][0]")
	  .Define("gem1_vz","hit.vz[ prm_e && hit.det==32 && hit.trid==main_trid][0]")
	  .Define("gem2_trid","hit.trid[ prm_e && hit.det==33 && hit.trid==main_trid][0]")
          .Define("gem2_r","hit.r[ prm_e && hit.det==33 && hit.trid==main_trid][0]").Define("gem2_ph","hit.ph[ prm_e && hit.det==33 && hit.trid==main_trid][0]")
	  .Define("gem2_x","hit.x[ prm_e && hit.det==33 && hit.trid==main_trid][0]").Define("gem2_y","hit.y[ prm_e && hit.det==33 && hit.trid==main_trid][0]")
	  .Define("gem2_px","hit.px[ prm_e && hit.det==33 && hit.trid==main_trid][0]").Define("gem2_py","hit.py[ prm_e && hit.det==33 && hit.trid==main_trid][0]")
	  .Define("gem2_pz","hit.pz[ prm_e && hit.det==33 && hit.trid==main_trid][0]").Define("gem2_k","hit.k[ prm_e && hit.det==33 && hit.trid==main_trid][0]")
	  .Define("gem3_trid","hit.trid[ prm_e && hit.det==34 && hit.trid==main_trid][0]")
          .Define("gem3_r","hit.r[ prm_e && hit.det==34 && hit.trid==main_trid][0]").Define("gem3_ph","hit.ph[ prm_e && hit.det==34 && hit.trid==main_trid][0]")
	  .Define("gem3_x","hit.x[ prm_e && hit.det==34 && hit.trid==main_trid][0]").Define("gem3_y","hit.y[ prm_e && hit.det==34 && hit.trid==main_trid][0]")
	  .Define("gem3_px","hit.px[ prm_e && hit.det==34 && hit.trid==main_trid][0]").Define("gem3_py","hit.py[ prm_e && hit.det==34 && hit.trid==main_trid][0]")
	  .Define("gem3_pz","hit.pz[ prm_e && hit.det==34 && hit.trid==main_trid][0]").Define("gem3_k","hit.k[ prm_e && hit.det==34 && hit.trid==main_trid][0]")
	  .Define("gem4_trid","hit.trid[ prm_e && hit.det==35 && hit.trid==main_trid][0]")
          .Define("gem4_r","hit.r[ prm_e && hit.det==35 && hit.trid==main_trid][0]").Define("gem4_ph","hit.ph[ prm_e && hit.det==35 && hit.trid==main_trid][0]")
	  .Define("gem4_x","hit.x[ prm_e && hit.det==35 && hit.trid==main_trid][0]").Define("gem4_y","hit.y[ prm_e && hit.det==35 && hit.trid==main_trid][0]")
	  .Define("gem4_px","hit.px[ prm_e && hit.det==35 && hit.trid==main_trid][0]").Define("gem4_py","hit.py[ prm_e && hit.det==35 && hit.trid==main_trid][0]")
	  .Define("gem4_pz","hit.pz[ prm_e && hit.det==35 && hit.trid==main_trid][0]").Define("gem4_k","hit.k[ prm_e && hit.det==35 && hit.trid==main_trid][0]")
          .Define("tg_th","part.th[part.trid==main_trid][0]").Define("tg_ph","part.ph[part.trid==main_trid][0]").Define("tg_p","part.p[part.trid==main_trid][0]")
	  .Define("tg_vx","part.vx[part.trid==main_trid][0]").Define("tg_vy","part.vy[part.trid==main_trid][0]").Define("tg_vz","part.vz[part.trid==main_trid][0]")
	  .Define("tg_trid","part.trid[part.trid==main_trid][0]").Define("tg_pid","part.pid[part.trid==main_trid][0]");

    df_small.Snapshot("newT",outFileName,{ "sieve_r", "sieve_ph", "main_r", "main_ph", "main_trid", "main_x", "main_y", "main_px", "main_py", "main_pz",
                                                   "rate" , "gem1_r", "gem1_ph", "sieve_ph", "sieve_px", "sieve_py", "sieve_pz", "gem1_x", "gem1_y", "gem4_x", 
                                                   "gem4_y","gem1_px", "gem1_py", "gem1_pz", "sieve_x", "sieve_y", "tg_th", "tg_ph", "tg_p", "tg_vz"});
}
