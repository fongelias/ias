# IAS Project Commands

## Custom Slash Commands

### /project:generate-samples

Creates a samples.js file with sample mappings in the project format.

**Usage:**
```
/project:generate-samples {folder_name} {sample1:file1.wav} {sample2:file2.wav} ...
```

**Example:**
```
/project:generate-samples ST-16 kick_drum:Kick.wav snare_hit:Snare.wav hi_hat:HiHat.wav bass_synth:Bass.wav
```

This command will:
1. Create the `converted/{folder_name}/` directory if it doesn't exist
2. Generate a `samples.js` file with the proper format matching existing sample files
3. Convert sample names to snake_case for consistency with the codebase
4. Include the GitHub repository reference

**Output:**
Creates `converted/ST-16/samples.js` with content like:
```javascript
samples({
  kick_drum: { 'b1': 'ST-16/Kick.wav' },
  snare_hit: { 'b1': 'ST-16/Snare.wav' },
  hi_hat: { 'b1': 'ST-16/HiHat.wav' },
  bass_synth: { 'b1': 'ST-16/Bass.wav' }
}, 'github:fongelias/ias/main/converted')
```