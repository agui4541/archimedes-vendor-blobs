echo "factory record test"

tinymix "Audio_AMIC_DCC_Setting" On
tinymix "Audio_ADC_1_Switch" On
tinymix "Audio_ADC_2_Switch" On
tinymix "Audio_Preamp1_Switch" IN_ADC1
tinymix "Audio_Preamp2_Switch" IN_ADC3

tinycap $1 -D 0 -d 1 -c 2 -r $2 -b 16 -p 512 -n 6 -T $3

pkill -f tinycap

tinymix "Audio_AMIC_DCC_Setting" On
tinymix "Audio_ADC_1_Switch" Off
tinymix "Audio_ADC_2_Switch" Off
tinymix "Audio_Preamp1_Switch" OPEN
tinymix "Audio_Preamp2_Switch" OPEN