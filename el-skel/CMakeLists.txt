# Declare the package name:
atlas_subdir( MyAnalysis )

# Component(s) in the package:
atlas_add_root_dictionary (MyAnalysisLib
   MyAnalysisDictSource
   ROOT_HEADERS MyAnalysis/*.h Root/LinkDef.h
   EXTERNAL_PACKAGES ROOT )

# add the library itself:
atlas_add_library (MyAnalysisLib
   MyAnalysis/*.h MyAnalysis/*.ihh Root/*.cxx ${MyAnalysisDictSource}
   PUBLIC_HEADERS MyAnalysis
   INCLUDE_DIRS
   LINK_LIBRARIES EventLoop
   PRIVATE_LINK_LIBRARIES )
