How to generate rootfiles and CSV files:

1.) Generate root files using macro "scripts/Run_Example_Optics_100k.mac"

  a.) Typically for optics studies, we use 4 million thrown events for each configuration.
  
  b.) This macro file has options for all three optics targets, all five beam passes, and multiple different field maps.

2.) Combine all root files for each configuration.

  a.) Use the "hadd" command.
  
3.) Slim down each combined root file using the script "scripts/SlimGeneral_simple.C"
