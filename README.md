
# Notched Beam Section Check Web App

Interactive web application for analyzing composite CLT-Glulam notched beam sections with real-time calculations and visualizations.

## Features

- **Interactive Parameter Input**: Adjust all geometry, material properties, and loads via sidebar
- **Real-time Calculations**: All utilization ratios (U variables) update instantly
- **Visual Analysis**: 
  - Bar charts showing all utilization ratios
  - Cross-section visualizations for normal and fire conditions
  - Color-coded pass/fail indicators
- **Comprehensive Results**:
  - U_b: Bending utilization (normal)
  - U_v: Shear utilization (normal)
  - U_b_fire: Bending utilization (fire)
  - U_v_fire: Shear utilization (fire)
  - U_Delta_L: Live load deflection utilization
  - U_Delta_DL: Total load deflection utilization

## Installation

### Option 1: Using pip

```bash
pip install streamlit plotly pandas numpy
```

### Option 2: Using requirements file

Create a `requirements.txt` file:
```
streamlit>=1.28.0
plotly>=5.17.0
pandas>=2.0.0
numpy>=1.24.0
```

Then install:
```bash
pip install -r requirements.txt
```

## Running the App

Navigate to the directory containing `beam_checker_app.py` and run:

```bash
streamlit run beam_checker_app.py
```

The app will automatically open in your default web browser at `http://localhost:8501`

## Usage

1. **Adjust Inputs**: Use the sidebar on the left to modify:
   - Geometry parameters (depth, width, notch dimensions)
   - Material properties (strength values, elastic moduli)
   - Demand values (moments, shears)
   - Adjustment factors (K, φ, λ, γ values)
   - Deflection parameters (span, loads, limits)

2. **View Results**: The main panel has 4 tabs:
   - **Utilization Summary**: Table showing all U values with pass/fail status
   - **Visual Results**: Interactive charts and cross-section diagrams
   - **Section Properties**: Calculated section properties for normal and fire conditions
   - **Detailed Calculations**: Step-by-step calculation breakdowns

3. **Interpretation**: 
   - ✅ **U < 1.0 = PASS** (design is adequate)
   - ❌ **U ≥ 1.0 = FAIL** (design needs revision)

## Default Values

The app is pre-loaded with the values from your original notebook:
- 24" x 22" composite section
- 5.5" CLT depth with 5" bearing notches
- SP 24F-V3 glulam material properties
- Normal and fire condition load cases

## Tips

- All inputs update calculations in real-time
- Hover over chart elements for detailed values
- Use the cross-section visualizations to understand geometry changes
- Export results by taking screenshots or using your browser's print function

## Technical Details

- Built with Streamlit for reactive web interface
- Plotly for interactive visualizations
- Follows NDS (National Design Specification) for Wood Construction
- Implements ASD (Allowable Stress Design) methodology

## Contact

For questions or issues, please refer to the original Jupyter notebook documentation.
