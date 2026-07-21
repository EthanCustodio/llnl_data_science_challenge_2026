from fastmcp import FastMCP
import numpy as np
from pathlib import Path
from skeletonization import skeletonize_mask

# Initialize the MCP server
mcp = FastMCP("CT Segmentation")

@mcp.tool()
def segment_ct_dataset(input_filepath: str, output_filepath: str, threshold: float) -> str:
    """
    Segments a 3D CT dataset based on a given density threshold value.
    
    Args:
        input_filepath: Path to the input .npy file containing the 3D CT scan data.
        output_filepath: Path indicating where the segmented .npy file should be saved.
        threshold: The density value to use as a threshold. Voxels >= threshold will be set to 1, others to 0.
    
    Returns:
        A status message indicating success and the save location, or an error message.
    """
    try:
        input_path = Path(input_filepath)
        output_path = Path(output_filepath)
        input_data = np.load(input_path, allow_pickle=False)

        if input_data.ndim != 3:
            return f"Error: expected a 3D CT dataset, but received shape {input_data.shape}."
        if not np.isfinite(threshold):
            return "Error: threshold must be a finite number."

        segmented_data = (input_data >= threshold).astype(np.uint8)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        np.save(output_path, segmented_data, allow_pickle=False)

        return f"Segmentation completed successfully. Segmented data saved to {output_filepath}."
    except (OSError, ValueError, TypeError) as error:
        return f"Error: unable to segment CT dataset: {error}"

@mcp.tool()
def visualize_slice(input_filepath: str, output_filepath: str, slice_index: int, axis: int = 0) -> str:
    """
    Loads a 3D CT dataset from a .npy file and saves a visualization of a specific slice to an image file.
    
    Args:
        input_filepath: Path to the input .npy file containing the 3D CT data.
        output_filepath: Path indicating where the output image should be saved (e.g., .png).
        slice_index: The index of the slice to visualize.
        axis: The axis along which to take the slice (0, 1, or 2). Default is 0.
        
    Returns:
        A status message indicating success and the save location, or an error message.
    """
    try:
        if axis not in (0, 1, 2):
            return "Error: axis must be 0, 1, or 2."

        input_path = Path(input_filepath)
        output_path = Path(output_filepath)
        input_data = np.load(input_path, allow_pickle=False)

        if input_data.ndim != 3:
            return f"Error: expected a 3D CT dataset, but received shape {input_data.shape}."
        if not 0 <= slice_index < input_data.shape[axis]:
            return (
                f"Error: slice_index must be between 0 and "
                f"{input_data.shape[axis] - 1} for axis {axis}."
            )

        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        image_data = np.take(input_data, slice_index, axis=axis)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        figure, plot_axis = plt.subplots(figsize=(8, 8))
        image = plot_axis.imshow(image_data, cmap="gray", origin="lower")
        plot_axis.set_title(f"Axis {axis}, slice {slice_index}")
        plot_axis.set_xlabel("Voxel index")
        plot_axis.set_ylabel("Voxel index")
        figure.colorbar(image, ax=plot_axis, label="Density")
        figure.tight_layout()
        figure.savefig(output_path, dpi=200, bbox_inches="tight")
        plt.close(figure)

        return f"Slice visualization completed successfully. Image saved to {output_filepath}."
    except (OSError, ValueError, TypeError, ImportError) as error:
        return f"Error: unable to visualize CT slice: {error}"

@mcp.tool()
def skeletonize(input_filepath: str, output_filepath: str) -> str:
    """
    Creates a skeleton from a 3D segmentation mask.
    
    Args:
        input_filepath: Path to the .npy file containing the 3D mask.
        output_filepath: Path to save the extracted skeleton (.npy).
        
    Returns:
        A status message indicating success and the save location, or an error message.
    """
    # pass # Implementation goes here, calling skeletonize_mask internally
    skeletonize_mask(input_filepath, output_filepath)
    return f"Skeletonization completed successfully. Skeleton saved to {output_filepath}."

if __name__ == "__main__":
    # Run the FastMCP server, exposing the tools over standard I/O (default)
    mcp.run()
