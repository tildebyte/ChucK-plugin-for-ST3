// arg(0) is the first argment after the name
Std.atoi(me.arg(0)) => int num_seconds;
me.arg(1) => string wav_name;

dac => Gain g => WvOut2 w => blackhole;
wav_name + ".wav" => w.wavFilename;
1 => w.record;
num_seconds::second => now;
0 => w.record;
