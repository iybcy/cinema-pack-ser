import c4d
import csv
import os

class KeyframeExporter:
    def __init__(self, filename):
        self.filename = filename

    def export_keyframes(self, obj):
        """Extract keyframe data from the provided object."""
        keyframe_data = []

        if not obj:
            raise ValueError("No object provided for keyframe extraction.")

        # Iterate through the object's animation tracks
        for track in obj.GetCTracks():
            curve = track.GetCurve()
            if curve:
                for i in range(curve.GetKeyCount()):
                    key = curve.GetKey(i)
                    time = key.GetTime().GetFrame(c4d.documents.GetActiveDocument().GetFps())
                    value = key.GetValue()
                    keyframe_data.append((time, value))
        
        return keyframe_data

    def write_to_csv(self, data, mode='w'):
        """Write the keyframe data to a CSV file."""
        if not data:
            raise ValueError("No data to write to CSV.")

        with open(self.filename, mode=mode, newline='') as file:
            writer = csv.writer(file)
            if mode == 'w':
                writer.writerow(['Frame', 'Value'])  # Write header only for new file
            writer.writerows(data)  # Write data rows

def main():
    # Example usage within CINEMA 4D environment
    try:
        doc = c4d.documents.GetActiveDocument()
        selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)

        if not selected_objects:
            raise RuntimeError("No objects selected for export.")

        exporter = KeyframeExporter('keyframe_data.csv')
        first_object = True

        # Iterate over each selected object and export keyframes
        for obj in selected_objects:
            keyframe_data = exporter.export_keyframes(obj)
            if keyframe_data:  # Only write if there's data
                mode = 'w' if first_object else 'a'
                exporter.write_to_csv(keyframe_data, mode)
                first_object = False

        print("Keyframe data exported successfully.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# This script should be run within the CINEMA 4D environment
if __name__ == "__main__":
    main()
