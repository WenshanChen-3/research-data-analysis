# an explanation of XPS Attenuation Model — What it is, when to use it, and what data you need

1. What this model does
This model estimates the thickness of a uniform overlayer on a semi-infinite substrate from XPS data.  
It uses the standard exponential attenuation (Beer–Lambert) law for photoelectrons leaving the sample, with explicit take-off angle dependence.

-It provides us:
1). closed-form expressions for a thin overgrown layer and substrate intensities  
2). the intensity ratio(R) of the overgrown layer and the substrate  
3). single-angle and multi-angle thickness fits  


2. When to use such model
Use this model when all of the following are approximately true:
- Geometry: A laterally uniform, planar film of thickness d on a semi-infinite substrate.  
- Homogeneous layers: No strong compositional gradients or buried roughness steps dominating the signal.  
- Known lines: You integrate well-resolved core lines for the overgrown layer element and the substrate element.  
- Comparable conditions: Both signals are acquired under the same instrument settings (photon energy, pass energy, analyzer, etc.) or corrected via sensitivity factors.  


3. When not to use it (or use with caution)
- Severe roughness or island growth (effective path lengths vary strongly).  
- Intermixing or graded composition near the interface.  
- Charging or energy-dependent transmission not corrected.  
- Overlayers thinner than a few Å where elastic scattering dominates.  
- Very thick films where the substrate signal is at the noise floor (unstable ratio).  


4. What data you must prepare before using the code

1). Background-subtracted peak areas
- Integrate the overgrown layer line area and substrate line area.  
- Apply a consistent background (e.g. Shirley or Tougaard) and deconvolution if needed.  
- Use identical acquisition conditions for both peaks.  

2). Take-off angle
- Angle between the surface normal and the analyzer (0° = normal emission).  
- For multi-angle analysis, prepare {θᵢ, integration of both film and sub. area}.  

3). Sensitivity factors(S) and scaling
-S is material- and instrument- dependent, when use CasaXPS, or any online database as reference, one should consider the specific instrument too. 

4). Effective atomic (or proportional) densities(n)
- Often set to 1.0 if relative scaling is absorbed into sensitivity factors.  

5). Inelastic mean free paths (IMFPs)--lambda
- IMFP related to material properties, e.g., valance band electrons, densities, kinetic energy etc.
- One could estimate the IMFPs in Quases(http://www.quases.com/products/quases-imfp-tpp2m/)

