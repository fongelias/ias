#!/usr/bin/env python3
"""
Convert raw 8-bit signed mono audio files to WAV format.
Based on the review from sroccaserra on Archive.org for the AmigaSTXX collection.
"""

import os
import sys
import struct
import wave
from pathlib import Path

def convert_raw_to_wav(input_file, output_file, sample_rate=8000):
    """
    Convert a raw 8-bit signed mono audio file to WAV format.
    
    Args:
        input_file: Path to input raw audio file
        output_file: Path to output WAV file
        sample_rate: Sample rate for the audio (default 8000 Hz for Amiga samples)
    """
    try:
        # Read the raw audio data
        with open(input_file, 'rb') as f:
            raw_data = f.read()
        
        if not raw_data:
            print(f"Warning: {input_file} is empty, skipping...")
            return False
            
        # Convert 8-bit signed to 16-bit signed for better compatibility
        # Raw 8-bit signed values range from -128 to 127
        audio_data = []
        for byte in raw_data:
            # Convert unsigned byte to signed byte
            signed_byte = byte if byte < 128 else byte - 256
            # Scale to 16-bit range
            scaled_value = signed_byte * 256
            audio_data.append(scaled_value)
        
        # Pack as 16-bit signed integers
        packed_data = b''.join(struct.pack('<h', sample) for sample in audio_data)
        
        # Create WAV file
        with wave.open(output_file, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
            wav_file.setframerate(sample_rate)
            wav_file.setnframes(len(audio_data))
            wav_file.writeframes(packed_data)
        
        print(f"Converted: {input_file} -> {output_file}")
        return True
        
    except Exception as e:
        print(f"Error converting {input_file}: {str(e)}")
        return False

def has_8svx_header(file_path):
    """
    Check if file has 8SVX format header (some files already have headers).
    """
    try:
        with open(file_path, 'rb') as f:
            header = f.read(12)
            return b'FORM' in header and b'8SVX' in header
    except:
        return False

def convert_directory(input_dir, output_dir, sample_rate=8000):
    """
    Convert all raw audio files in a directory to WAV format.
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    converted_count = 0
    skipped_count = 0
    
    for file_path in input_path.iterdir():
        if file_path.is_file():
            # Skip files that already have 8SVX headers
            if has_8svx_header(file_path):
                print(f"Skipping {file_path.name} (already has 8SVX header)")
                skipped_count += 1
                continue
            
            # Convert to WAV
            output_file = output_path / f"{file_path.name}.wav"
            if convert_raw_to_wav(str(file_path), str(output_file), sample_rate):
                converted_count += 1
            else:
                skipped_count += 1
    
    print(f"\nDirectory {input_dir}: {converted_count} files converted, {skipped_count} files skipped")
    return converted_count, skipped_count

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python convert_to_aiff.py <input_file> [output_file] [sample_rate]")
        print("  python convert_to_aiff.py --batch <sounds_dir> [output_dir] [sample_rate]")
        print("\nExamples:")
        print("  python convert_to_aiff.py sounds/ST-XX/ST-01/Alien")
        print("  python convert_to_aiff.py --batch sounds/ST-XX/ST-01 converted/ST-01")
        print("  python convert_to_aiff.py --batch sounds/ST-XX converted")
        sys.exit(1)
    
    if sys.argv[1] == '--batch':
        # Batch conversion mode
        input_dir = sys.argv[2] if len(sys.argv) > 2 else 'sounds/ST-XX'
        output_dir = sys.argv[3] if len(sys.argv) > 3 else 'converted'
        sample_rate = int(sys.argv[4]) if len(sys.argv) > 4 else 8000
        
        input_path = Path(input_dir)
        
        if not input_path.exists():
            print(f"Error: Input directory {input_dir} does not exist")
            sys.exit(1)
        
        total_converted = 0
        total_skipped = 0
        
        # If input is ST-XX directory, process all subdirectories
        if input_path.name == 'ST-XX':
            for subdir in sorted(input_path.iterdir()):
                if subdir.is_dir():
                    sub_output_dir = Path(output_dir) / subdir.name
                    converted, skipped = convert_directory(subdir, sub_output_dir, sample_rate)
                    total_converted += converted
                    total_skipped += skipped
        else:
            # Process single directory
            total_converted, total_skipped = convert_directory(input_dir, output_dir, sample_rate)
        
        print(f"\nTotal: {total_converted} files converted, {total_skipped} files skipped")
        
    else:
        # Single file conversion mode
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else f"{input_file}.wav"
        sample_rate = int(sys.argv[3]) if len(sys.argv) > 3 else 8000
        
        if not os.path.exists(input_file):
            print(f"Error: Input file {input_file} does not exist")
            sys.exit(1)
        
        if has_8svx_header(input_file):
            print(f"File {input_file} already has 8SVX header, skipping conversion")
        else:
            convert_raw_to_wav(input_file, output_file, sample_rate)

if __name__ == '__main__':
    main()