// recording_instructions.ck

// arg(0) is the first argment after the name
Std.atoi(me.arg(0)) => int num_seconds;
me.arg(1) => string wav_name;

dac => WvOut2 w => blackhole;
wav_name + ".wav" => w.wavFilename;

1 => w.record;
num_seconds::second => now;
0 => w.record;

// i want to build in support for setting gain too. 
// simple gain will convert to mono, so it must be split.
