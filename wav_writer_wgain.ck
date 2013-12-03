// arg(0) is the first argment after the name
me.arg(0) => Std.atoi => int num_seconds;
me.arg(1) => string wav_name;
me.arg(2) => Std.atof => float max_amp;

dac => Mix2 regulator => WvOut2 w => blackhole;
regulator.gain(max_amp);

//"data/session" => w.autoPrefix;
wav_name + ".wav" => w.wavFilename;

1 => w.record;
num_seconds::second => now;
0 => w.record;

w.closeFile();
