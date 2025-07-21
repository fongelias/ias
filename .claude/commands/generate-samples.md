# Generate Samples Command

Generate a samples.js file for the IAS project with the specified folder name and sample mappings.

## Instructions

You will generate the contents of a samples.js file and output it for the user to copy, with the following specifications:

1. **Parse the arguments**: The arguments will be in the format: `{folder_name} {sample1:file1.wav} {sample2:file2.wav} ...`
2. **Convert sample names**: Convert sample names to snake_case for consistency with existing files
3. **Generate samples.js content**: Output the file contents with the exact format matching existing sample files
4. **DO NOT create files or directories**: Only output the generated code for the user to copy

## Format Requirements

The generated `samples.js` file must follow this exact format:

```javascript
samples({
  sample_name: { 'b1': 'folder_name/FileName.wav' },
  another_sample: { 'b1': 'folder_name/AnotherFile.wav' }
}, 'github:fongelias/ias/main/converted')
```

## Processing Rules

- Sample names should be converted to snake_case (e.g., "kick_drum", "snare_hit")
- Each sample entry has the format: `sample_name: { 'b1': 'folder_name/FileName.wav' }`
- The file must end with the GitHub repository reference
- Output the generated code in a code block for easy copying
- Do not create any files or directories

## Arguments to Process

$ARGUMENTS