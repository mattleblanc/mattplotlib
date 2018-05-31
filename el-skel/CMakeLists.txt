# The name of the package:
atlas_subdir (MyAnalysis)

# Add the shared library:
atlas_add_library (MyAnalysisLib
  MyAnalysis/*.h Root/*.cxx
  PUBLIC_HEADERS MyAnalysis
  LINK_LIBRARIES AnaAlgorithmLib)

# Add the dictionary:
atlas_add_dictionary (MyAnalysisDict
  MyAnalysis/MyAnalysisDict.h
  MyAnalysis/selection.xml
  LINK_LIBRARIES MyAnalysisLib)

if (NOT XAOD_STANDALONE)
  # Add a component library for AthAnalysis only:
  atlas_add_component (MyAnalysis
    src/components/*.cxx
    LINK_LIBRARIES MyAnalysisLib)
endif ()

# Install files from the package:
atlas_install_joboptions( share/*.py )
