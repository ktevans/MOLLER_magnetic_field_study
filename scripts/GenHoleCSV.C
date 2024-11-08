/////////////////////////////////////////////////////////////////////////////
// This script will read in a slimmed MOLLER Optics Root File and generate
// CSV files for each sieve hole image on the upstream gem plane based on
// r-phi fits.
// Script originally created by Vassu Doomra (2024) and edited to account for
// different magnetic field maps and sieve rotations by Kate Evans (Nov 2024)
/////////////////////////////////////////////////////////////////////////////

#include <TFile.h>
#include <TH1.h>
#include <TH2.h>
#include <TCanvas.h>
#include <list>
#include <vector>

// Define basic constants
const double pi = TMath::ACos(-1);
const double Me = 0.511; // mass of electron
const double Me2 = Me*Me;

// The sieve geometry is such that there are always 21 holes with 3 in each sector.
const int nholes = 21;
const int nsectors = 7;

// Define the upper and lower azimuthal bounds of each sector. These lists of seven values will be updated later.
double angle_lo[nsectors] = {-999};
double angle_up[nsectors] = {-999};

// Define histograms and finctions.
TF1* func = NULL; // fit to r hits
TF1* func1 = NULL; // fit to phi hits
TF1* func2 = NULL; // fit to r' hits
TF1* func3 = NULL; // fit to phi' hits

TH1D* radial[nholes] = {NULL};
TH1D* rprime[nholes] = {NULL};
TH1D* phiprime[nholes] = {NULL};
TH1D* phi[nholes] = {NULL};

TH2D* hist_rphi = {NULL};
TH2D* hist_rrprime = {NULL};
TH2D* hist_phi_phiprime = {NULL};

TH2D* h2d_r_phi[nholes] = {NULL};
TH2D* h2d_rprime_phi[nholes] = {NULL};
TH2D* h2d_phiprime_phi[nholes] = {NULL};

void GenHoleCSV(string infile, double rotation, const int cut = 0)
{

  gStyle->SetOptFit(1); // include fit information in stat boxes

  string sector_rotation = "";
  vector<string> holeNames(nholes);
  vector<double> central_sieve_r(nholes);
  vector<double> phi_lo(nholes);
  vector<double> phi_hi(nholes);

  // Read in the slimmed root file.
  TFile* f1 = new TFile(infile.c_str(), "READ");
  TTree* T1 = (TTree*)f1->Get("newT");

  int nevents = T1->GetEntries();

  // Check the sieve rotation. Based on how many degrees the sieve is rotated, the sieve hole positions and phi regions are assigned.
  if(rotation == 51.0)
  {
    sector_rotation = "1secRot";
    holeNames = {"21", "22", "23", "31", "32", "33", "41", "42", "43", "51", "52", "53", "61", "62", "63", "71", "72", "73", "11", "12", "13"};
    central_sieve_r = {50.0, 56.0, 75.0, 39.0, 63.0, 80.0, 50.0, 60.0, 70.0, 56.0, 56.0, 80.0, 39.0, 60.0, 75.0, 44.0, 68.0, 84.5, 35.0, 58.0, 84.5};
    phi_lo = {1.242,0.898,1.496,1.795,2.349,2.169,2.992,3.291,2.693,3.590,3.937,4.189,4.488,5.034,4.862,5.685,5.947,5.386,0.299,0.598,0.000};
    phi_hi = {1.496,1.242,1.795,2.169,2.693,2.349,3.291,3.590,2.992,3.937,4.189,4.488,4.862,5.386,5.034,5.947,6.283,5.685,0.598,0.898,0.299};
  }
  else if(rotation == 103.0)
  {
    sector_rotation = "2secRot";
    holeNames = {"31", "32", "33", "41", "42", "43", "51", "52", "53", "61", "62", "63", "71", "72", "73", "11", "12", "13", "21", "22", "23"};
    central_sieve_r = {39.0, 63.0, 80.0, 50.0, 60.0, 70.0, 56.0, 56.0, 80.0, 39.0, 60.0, 75.0, 44.0, 68.0, 84.5, 35.0, 58.0, 84.5, 50.0, 56.0, 75.0};
    phi_lo = {2.139,1.795,2.394,2.693,3.246,3.067,3.890,4.189,3.590,4.488,4.835,5.086,5.386,5.932,5.760,0.299,0.561,0.000,1.197,1.496,0.898};
    phi_hi = {2.394,2.139,2.693,3.067,3.590,3.246,4.189,4.488,3.890,4.835,5.086,5.386,5.760,6.283,5.932,0.561,0.898,0.299,1.496,1.795,1.197};
  }
  else if(rotation == 154.0)
  {
    sector_rotation = "3secRot";
    holeNames = {"41", "42", "43", "51", "52", "53", "61", "62", "63", "71", "72", "73", "11", "12", "13", "21", "22", "23", "31", "32", "33"};
    central_sieve_r = {50.0, 60.0, 70.0, 56.0, 56.0, 80.0, 39.0, 60.0, 75.0, 44.0, 68.0, 84.5, 35.0, 58.0, 84.5, 50.0, 56.0, 75.0, 39.0, 63.0, 80.0};
    phi_lo = {3.037,2.693,3.291,3.590,4.144,3.964,4.787,5.086,4.488,5.386,5.733,5.984,0.000,0.546,0.374,1.197,1.459,0.898,2.094,2.394,1.795};
    phi_hi = {3.291,3.037,3.590,3.964,4.488,4.144,5.086,5.386,4.787,5.733,5.984,6.283,0.374,0.898,0.546,1.459,1.795,1.197,2.394,2.693,2.094};
  }
  else if(rotation == 206.0)
  {
    sector_rotation = "4secRot";
    holeNames = {"51", "52", "53", "61", "62", "63", "71", "72", "73", "11", "12", "13", "21", "22", "23", "31", "32", "33", "41", "42", "43"};
    central_sieve_r = {56.0, 56.0, 80.0, 39.0, 60.0, 75.0, 44.0, 68.0, 84.5, 35.0, 58.0, 84.5, 50.0, 56.0, 75.0, 39.0, 63.0, 80.0, 50.0, 60.0, 70.0};
    phi_lo = {3.934,3.590,4.189,4.488,5.042,4.862,5.685,5.984,5.386,0.000,0.347,0.598,0.898,1.444,1.272,2.094,2.356,1.795,2.992,3.291,2.693};
    phi_hi = {4.189,3.934,4.488,4.862,5.386,5.042,5.984,6.283,5.685,0.347,0.598,0.898,1.272,1.795,1.444,2.356,2.693,2.094,3.291,3.590,2.992};
  }
  else if(rotation == 257.0)
  {
    sector_rotation = "5secRot";
    holeNames = {"61", "62", "63", "71", "72", "73", "11", "12", "13", "21", "22", "23", "31", "32", "33", "41", "42", "43", "51", "52", "53"};
    central_sieve_r = {39.0, 60.0, 75.0, 44.0, 68.0, 84.5, 35.0, 58.0, 84.5, 50.0, 56.0, 75.0, 39.0, 63.0, 80.0, 50.0, 60.0, 70.0, 56.0, 56.0, 80.0};
    phi_lo = {4.832,4.488,5.086,5.386,5.939,5.760,0.299,0.598,0.000,0.898,1.245,1.496,1.795,2.341,2.169,2.992,3.254,2.693,3.890,4.189,3.590};
    phi_hi = {5.086,4.832,5.386,5.760,6.283,5.939,0.598,0.898,0.299,1.245,1.496,1.795,2.169,2.693,2.341,3.254,3.590,2.992,4.189,4.488,3.890};
  }
  else if(rotation == 309.0)
  {
    sector_rotation = "6secRot";
    holeNames = {"71", "72", "73", "11", "12", "13", "21", "22", "23", "31", "32", "33", "41", "42", "43", "51", "52", "53", "61", "62", "63"};
    central_sieve_r = {44.0, 68.0, 84.5, 35.0, 58.0, 84.5, 50.0, 56.0, 75.0, 39.0, 63.0, 80.0, 50.0, 60.0, 70.0, 56.0, 56.0, 80.0, 39.0, 60.0, 75.0};
    phi_lo = {5.730,5.386,5.984,0.000,0.554,0.374,1.197,1.496,0.898,1.795,2.142,2.394,2.693,3.239,3.067,3.890,4.151,3.590,4.787,5.086,4.488};
    phi_hi = {5.984,5.730,6.283,0.374,0.898,0.554,1.496,1.795,1.197,2.142,2.394,2.693,3.067,3.590,3.239,4.151,4.488,3.890,5.086,5.386,4.787};
  }
  else if(rotation == 0.0)
  {
    sector_rotation = "0secRot";
    holeNames = {"11", "12", "13", "21", "22", "23", "31", "32", "33", "41", "42", "43", "51", "52", "53", "61", "62", "63", "71", "72", "73"};
    central_sieve_r = {35.0, 58.0, 84.5, 50.0, 56.0, 75.0, 39.0, 63.0, 80.0, 50.0, 60.0, 70.0, 56.0, 56.0, 80.0, 39.0, 60.0, 75.0, 44.0, 68.0, 84.5};
    phi_lo = {0.344, 0.000, 0.598, 0.898, 1.451, 1.272, 2.094, 2.394, 1.795, 2.693, 3.040, 3.291, 3.590, 4.136, 3.964, 4.787, 5.049, 4.488, 5.685, 5.984, 5.386};
    phi_hi = {0.598, 0.344, 0.898, 1.272, 1.795, 1.451, 2.394, 2.693, 2.094, 3.040, 3.291, 3.590, 3.964, 4.488, 4.136, 5.049, 5.386, 4.787, 5.984, 6.283, 5.685};
  }
  else
  {
    cout << "Not a valid sieve rotation. Options are: 0.0, 51.0, 103.0, 154.0, 206.0, 257.0, or 309.0." << endl;
  }

  // Create histograms for each sieve hole.
  for(int j=0; j<nholes; j++)
  {

    phi[j] = new TH1D(Form("phi_%s", holeNames[j].c_str()),"gem_phi_distribution;phi[rad];Counts",200, 0, 2*pi);

    phiprime[j] = new TH1D(Form("phiprime_%s", holeNames[j].c_str()),"gem_phi_prime_distribution;phi_prime[rad/mm];Counts",200, -0.02, 0.02);

    rprime[j] = new TH1D(Form("rprime_%s", holeNames[j].c_str()),"rprime_distribution;r_prime;Counts",300, 0.02, 0.08);

    h2d_r_phi[j] = new TH2D(Form("r_phi_%s", holeNames[j].c_str()),"r_phi_distribution;r[mm];phi[rad];Counts",500, 600, 1100, 200, 0, 2*pi);

    h2d_rprime_phi[j] = new TH2D(Form("rprime_phi_%s", holeNames[j].c_str()),"rprime_phi_distribution;r_prime;phi[rad];Counts", 500, 0 , 0.1, 200, 0, 2*pi);

    h2d_phiprime_phi[j] = new TH2D(Form("phiprime_phi_%s", holeNames[j].c_str()),"phiprime_phi_distribution;phi_prime[rad/mm];phi[rad];Counts", 500, -0.02 , 0.02, 200, 0, 2*pi);

  } // end loop through holes

  // These histograms include information from ALL the sieve holes.
  hist_rrprime = new TH2D("hist_rrprime", "GEM r-r' Distribtuion", 500, 0, 0.1, 500, 0, 7);
  hist_phi_phiprime = new TH2D("hist_phi_phiprime", "GEM phi-phi' Distribtuion", 500, -0.02, 0.02, 500, 0, 7);

  double energy_cut = -999;
  string targetName;
  string passName;
  string fieldMap;

  // List out the possible targets. Make sure that the root file being read in has the correct target name in it.

  if(infile.find("Optics1") != std::string::npos) targetName = "Optics1"; //Optics1 = US
  else if(infile.find("Optics2") != std::string::npos) targetName = "Optics2"; //Optics2 = DS
  else if(infile.find("Optics3") != std::string::npos) targetName = "Optics3";//Optics3 = MS
  else if(infile.find("opticsUM") != std::string::npos) targetName = "C12_opticsUM";
  else if(infile.find("opticsUS") != std::string::npos) targetName = "C12_opticsUS";
  else if(infile.find("LH2") != std::string::npos) targetName = "LH2";

  // List out magnetic field maps. Make sure that the root file being read in has the correct field map name in it.

  if(infile.find("Symmetric") != std::string::npos) fieldMap = "Symmetric";

  else if(infile.find("DipolePoint5RandSC23") != std::string::npos) fieldMap = "DipolePoint5RandSC23";
  else if(infile.find("Dipole3SameSC23") != std::string::npos) fieldMap = "Dipole3SameSC23";

  else if(infile.find("A2mm_inward") != std::string::npos) fieldMap = "A2mm_inward";
  else if(infile.find("A1mm_inward") != std::string::npos) fieldMap = "A1mm_inward";
  else if(infile.find("A1mm_outward") != std::string::npos) fieldMap = "A1mm_outward";
  else if(infile.find("A2mm_outward") != std::string::npos) fieldMap = "A2mm_outward";
  else if(infile.find("A3mm_outward") != std::string::npos) fieldMap = "A3mm_outward";
  else if(infile.find("A4mm_outward") != std::string::npos) fieldMap = "A4mm_outward";

  // ^^^ Add more fieldmaps as needed

  // Name the path that the output CSV files will be sent to. Change this to match your volatile directory.

  string pathName = "/volatile/halla/moller12gev/ktevans1/rootfiles2024/MagFieldStudy/" + fieldMap +"/output/";

  cout << targetName << endl;
  cout << fieldMap << endl;
  cout << pathName << endl;

  // DOES THIS NEED TO CHANGE TO ACCOUNT FOR ROTATIONS???
  for(int ii = 0; ii < nsectors; ii++){

    angle_lo[ii] = ii*2*pi/7;
    angle_up[ii] = (ii+1)*2*pi/7;

  }

  // Check the energy pass to make proper energy cut. Make sure that the input root file has the pass name in it in the form "Pass#" where # is 1, 2, 3, 4, or 5.
  if(infile.find("Pass1") != std::string::npos)
  {

    energy_cut = 2200.;
    passName = "p1";
    hist_rphi = new TH2D("hist_rphi", "GEM r-#phi Distribtuion", 600, 800, 1100, 500, 0, 7);

    for(int j=0; j<nholes; j++)
    {
      radial[j] = new TH1D(Form("r_%s", holeNames[j].c_str()),"gem_r_distribution;r[mm];Counts",600, 800, 1100);
      r_canvas[j] = new TCanvas(Form("r_%s", holeNames[j].c_str()));
     } // end for loop

  } // end pass1

  else if(infile.find("Pass2") != std::string::npos)
  {

    energy_cut = 4400.;
    passName = "p2";
    hist_rphi = new TH2D("hist_rphi", "GEM r-#phi Distribtuion", 800, 700, 1100, 500, 0, 7);

    for(int j=0; j<nholes; j++)
    {
      radial[j] = new TH1D(Form("r_%s", holeNames[j].c_str()),"gem_r_distribution;r[mm];Counts",800, 700, 1100);
      r_canvas[j] = new TCanvas(Form("r_%s", holeNames[j].c_str()));
    }

  } // end pass 2

  else if(infile.find("Pass3") != std::string::npos)
  {

    energy_cut = 6600.;
    passName = "p3";
    hist_rphi = new TH2D("hist_rphi", "GEM r-#phi Distribtuion", 600, 600, 900, 500, 0, 7);

    for(int j=0; j<nholes; j++)
    {
      radial[j] = new TH1D(Form("r_%s", holeNames[j].c_str()),"gem_r_distribution;r[mm];Counts",600, 600, 900);
      r_canvas[j] = new TCanvas(Form("r_%s", holeNames[j].c_str()));
    }

  } // end pass 3

  else if(infile.find("Pass4") != std::string::npos)
  {

    energy_cut = 8800.;
    passName = "p4";
    hist_rphi = new TH2D("hist_rphi", "GEM r-#phi Distribtuion", 400, 600, 800, 500, 0, 7);

    for(int j=0; j<nholes; j++)
    {
      radial[j] = new TH1D(Form("r_%s", holeNames[j].c_str()),"gem_r_distribution;r[mm];Counts",400, 600, 800);
      r_canvas[j] = new TCanvas(Form("r_%s", holeNames[j].c_str()));
    }

  } // end pass 4

  else if(infile.find("Pass5") != std::string::npos)
  {

    energy_cut = 11000.;
    passName = "p5";
    hist_rphi = new TH2D("hist_rphi", "GEM r-#phi Distribtuion", 800, 650, 1050, 500, 0, 7);

    for(int j=0; j<nholes; j++)
    {
      radial[j] = new TH1D(Form("r_%s", holeNames[j].c_str()),"gem_r_distribution;r[mm];Counts",800, 650, 1050);
      r_canvas[j] = new TCanvas(Form("r_%s", holeNames[j].c_str()));
    }

  } // end pass 5

  else
  {
    cout << "Your root file is not properly named. Please make sure that it contains the energy pass in the form 'Pass#', where # is 1, 2, 3, 4, or 5." << endl;
  }

  // Plot with proper error bars???
  hist_rphi->Sumw2();
  hist_rrprime->Sumw2();
  hist_phi_phiprime->Sumw2();

  // Define new root tree with slimmed variables
  double sieve_r, gem_r, gem_ph, rate, tg_th, tg_p, tg_ph, tg_vz, gem_px, gem_py, gem_pz, gem_x, gem_y;

  T1->SetBranchAddress("sieve_r",&sieve_r);
  T1->SetBranchAddress("gem1_r",&gem_r);
  T1->SetBranchAddress("gem1_ph",&gem_ph);
  T1->SetBranchAddress("gem1_px",&gem_px);
  T1->SetBranchAddress("gem1_py",&gem_py);
  T1->SetBranchAddress("gem1_pz",&gem_pz);
  T1->SetBranchAddress("gem1_x",&gem_x);
  T1->SetBranchAddress("gem1_y",&gem_y);
  T1->SetBranchAddress("rate",&rate);
  T1->SetBranchAddress("tg_th",&tg_th);
  T1->SetBranchAddress("tg_ph",&tg_ph);
  T1->SetBranchAddress("tg_p",&tg_p);
  T1->SetBranchAddress("tg_vz",&tg_vz);

  for(int j=0; j<nevents; j++)
  {

    T1->GetEntry(j);
    int index_hole = -999;

    rate = rate/200; // WHY ARE WE DIVIDING THE RATE????

    if(sieve_r < 26.5) continue; // don't look at particles that go through the sieve inner bore
    double gem_k = sqrt(gem_px*gem_px + gem_py*gem_py + gem_pz*gem_pz + Me2);

    // Make a very tight energy cut on particles. Match the scattered electrons' 4-momentum magnitude to the beam energy. If particles are within 2MeV then keep them.
    if(cut && fabs(gem_k - energy_cut) > 2) continue;

    // Shift the phi values to be 0 to 2pi instead of -pi to pi.
    if(gem_ph<0) gem_ph += 2*pi;

    // Assign hole index to events based on their phi locations.
    // MAKE SURE THIS WORKS FOR DIFFERENT ROTATIONS!!!!
    for(int l=0; l<nholes; l++)
    {

      if(gem_ph > phi_lo[l] && gem_ph < phi_hi[l])
      {

        index_hole = l; // if an event hits the gems within a specified phi region then it is assigned to a specified hole.

      }//end if

    }//end for loop

    // Define r' and phi' as dr/dz and dphi/dz.
    double r_prime = (gem_x*gem_px + gem_y*gem_py)/(gem_r*gem_pz);
    double phi_prime = (-gem_y*gem_px+gem_x*gem_py)/(gem_r*gem_pz);

    if (index_hole ==-999) continue; // if the gem_ph value did not meet the above criteria, then index_hole will still be -999, and we should move on to the next event

    radial[index_hole]->Fill(gem_r, rate);
    rprime[index_hole]->Fill(r_prime, rate);
    phi[index_hole]->Fill(gem_ph, rate);
    phiprime[index_hole]->Fill(phi_prime, rate);

    hist_rphi->Fill(gem_r, gem_ph);
    hist_rrprime->Fill(r_prime, gem_ph);
    hist_phi_phiprime->Fill(phi_prime, gem_ph);

  } // end loop over entries

  // Draw your histograms.

  TCanvas* c1 = new TCanvas();
  c1->cd();
  hist_rphi->Draw("colz");

  TCanvas* c2 = new TCanvas();
  c2->cd();
  hist_rrprime->Draw("colz");

  TCanvas* c3 = new TCanvas();
  c3->cd();
  hist_phi_phiprime->Draw("colz");

  for(int ihole = 0; ihole < nholes; ihole++)
  {

    if (!radial[ihole])
    {
      continue;
    }

    if (radial[ihole])
    {

      // Write output to a CSV file.
      std::ofstream csvFile;

      // If there are fewer than 50 events in a given hole image, then continue to the next hole. We don't need to analyze a sieve hole image with so few events.
      if(radial[ihole]->GetEntries() < 50) continue;

      string fileName = pathName + fieldMap + "_" + passName + "_" + targetName + "_" + sector_rotation + "_" + holeNames[ihole] + ".csv";

      cout << fileName << endl;

      csvFile.open(fileName, std::ofstream::app);

      // List the CSV column headers.
      csvFile << "tg_th" << "," << "tg_ph" << "," << "tg_p" << "," << "tg_vz" << "," << "sieve_r" << "," << "gem_r" << "," << "r_prime" << "," << "gem_ph" << "," << "phi_prime" << endl;

      // First, fit to r.

      // If you want to look at the events that do NOT include the radiative tail on the sieve hole image, then you want to make the cut which cuts out all events whose energies differ from the beam energy by more than 2MeV.
      if(cut)
      {

        radial[ihole]->GetXaxis()->SetRangeUser(radial[ihole]->GetMean()-5*radial[ihole]->GetRMS(), radial[ihole]->GetMean()+5*radial[ihole]->GetRMS());

        func = new TF1("func", "gaus",radial[ihole]->GetMean()-2.0*radial[ihole]->GetRMS(),radial[ihole]->GetMean()+2.0*radial[ihole]->GetRMS());

      }

      else
      {

        radial[ihole]->GetXaxis()->SetRangeUser(radial[ihole]->GetMean()-2.5*radial[ihole]->GetRMS(), radial[ihole]->GetMean()+1.0*radial[ihole]->GetRMS());

        rprime[ihole]->GetXaxis()->SetRangeUser(rprime[ihole]->GetMean()-2.5*rprime[ihole]->GetRMS(), rprime[ihole]->GetMean()+1.0*rprime[ihole]->GetRMS());

        func = new TF1("func", "gaus",radial[ihole]->GetMean()-2.5*radial[ihole]->GetRMS(),radial[ihole]->GetMean()+1.5*radial[ihole]->GetRMS());

      }

      // Fit a gaussian to the 1d radial plots for each hole. This will help define what radial range to look in for each hole.
      radial[ihole]->Fit(func,"RQ");
      // "RQ" are the fit options. "R" says to use the range specified in the function range, and "Q" says to print in quiet mode, i.e., don't print out the fit parameters to your terminal while the script it running.

      // Fit gaussians iteratively.
      for(int itr = 0; itr < 5; itr++)
      {

        radial[ihole]->Fit(func, "RQ","",func->GetParameter(1)-2.0*func->GetParameter(2),func->GetParameter(1)+2.0*func->GetParameter(2));

      }

      // Update your plot to include fit and fit stats.
      gPad->Modified(); gPad->Update();

      // Now, we fit to phi
      func1 = new TF1("func1", "gaus", phi_lo[ihole], phi_hi[ihole]);
      phi[ihole]->Fit(func1,"RQ");

      gPad->Modified(); gPad->Update();

      // Now, fit to r'
      func2 = new TF1("func2", "gaus", rprime[ihole]->GetMean()-2.5*rprime[ihole]->GetRMS(), rprime[ihole]->GetMean()+1.0*rprime[ihole]->GetRMS());

      for(int itr = 0; itr < 5; itr++)
      {

        rprime[ihole]->Fit(func2, "RQ","",func2->GetParameter(1)-2.0*func2->GetParameter(2),func2->GetParameter(1)+2.0*func2->GetParameter(2));

      }

      gPad->Modified(); gPad->Update();

      // Now, fit to phi'
      func3 = new TF1("func3", "gaus", phiprime[ihole]->GetMean()-2.5*phiprime[ihole]->GetRMS(), phiprime[ihole]->GetMean()+1.0*phiprime[ihole]->GetRMS());
      phiprime[ihole]->Fit(func3,"RQ");

      gPad->Modified(); gPad->Update();

      // Use the gaussian parameters to define bounds on our variables. This uses a 2-sigma cut around the mean for r, phi, r', and phi', but it may be better to use a 2.5-sigma or even 3-sigma cut.
      double lower_r = func->GetParameter(1) - 2*func->GetParameter(2);
      double upper_r = func->GetParameter(1) + 2*func->GetParameter(2);

      double lower_phi = func1->GetParameter(1) - 2*func1->GetParameter(2);
      double upper_phi = func1->GetParameter(1) + 2*func1->GetParameter(2);

      double lower_rprime = func2->GetParameter(1) - 2*func2->GetParameter(2);
      double upper_rprime = func2->GetParameter(1) + 2*func2->GetParameter(2);

      double lower_phiprime = func3->GetParameter(1) - 2*func3->GetParameter(2);
      double upper_phiprime = func3->GetParameter(1) + 2*func3->GetParameter(2);

      // This loops through the events again and plots within the bounds we found from the 1d fits, but code is repeated here. There should be a better way to do this.
      for(int j=0; j<nevents; j++)
      {

        T1->GetEntry(j);

        // Repeated code:
        // -----
        if(sieve_r < 26.5) continue;

        double gem_k = sqrt(gem_px*gem_px + gem_py*gem_py + gem_pz*gem_pz + Me2);

        if(cut && fabs(gem_k - energy_cut) > 2) continue;

        if(gem_ph<0) gem_ph += 2*pi;

        double r_prime = (gem_x*gem_px + gem_y*gem_py)/(gem_r*gem_pz);
        double phi_prime = (-gem_y*gem_px+gem_x*gem_py)/(gem_r*gem_pz);
        // -----

        // Check if particles hit within bounds and fill rate weighted histograms.
        if( (gem_r > lower_r && gem_r < upper_r) && (gem_ph > lower_phi && gem_ph < upper_phi) )
        {

          h2d_r_phi[ihole]->Fill(gem_r, gem_ph, rate);

        }

        if( (r_prime > lower_rprime && r_prime < upper_rprime) && (gem_ph > lower_phi && gem_ph < upper_phi) )
        {

          h2d_rprime_phi[ihole]->Fill(r_prime, gem_ph, rate);

        }

        if( (phi_prime > lower_phiprime && phi_prime < upper_phiprime) && (gem_ph > lower_phi && gem_ph < upper_phi) )
        {
          h2d_phiprime_phi[ihole]->Fill(phi_prime, gem_ph, rate);
        }

        // Check that a hit matches all the conditions and then writ it to the CSV file.
        if((gem_r > lower_r && gem_r < upper_r) && (gem_ph > lower_phi && gem_ph < upper_phi) && (r_prime > lower_rprime && r_prime < upper_rprime) && (phi_prime > lower_phiprime && phi_prime < upper_phiprime))
        {

          csvFile << tg_th << "," << tg_ph << "," << tg_p << "," << tg_vz << "," << sieve_r << "," << gem_r << "," << r_prime << "," << gem_ph << "," << phi_prime << endl;

        }

      } // end loop through entries

      cout << "Hole " << holeNames[ihole] << " Analysis Complete" << endl;
    } // end if for histogram null check

  } // end loop over holes

  // Name the output root file.
  string outfileName = pathName + fieldMap + "_" + passName + "_" + targetName + "_" + sector_rotation + "_plots.root";

  // Name the file differently if you make the tight energy cut.
  if(cut) outfileName = pathName + fieldMap + "_" + passName + "_" + targetName + "_" + sector_rotation + "_plots_non_radiative.root";

  TFile* fout = new TFile(outfileName.c_str(),"RECREATE");
  fout->cd();

  // Write out all the histograms to a root file.
  for(int ihole = 0; ihole < nholes; ihole++)
  {
    if (!radial[ihole])
    {
      continue;
    }
    if (radial[ihole])
    {
      radial[ihole]->Write();
      h2d_r_phi[ihole]->Write();
      h2d_rprime_phi[ihole]->Write();
      h2d_phiprime_phi[ihole]->Write();
      phi[ihole]->Write();
      rprime[ihole]->Write();
      phiprime[ihole]->Write();
    }
  }

  hist_rphi->Write();
  hist_rrprime->Write();
  hist_phi_phiprime->Write();

  cout << "Plots have been sent to " << outfileName << endl;

} // end main
