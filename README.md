# rtviz

**rtviz** is a program for visualizing reading times with an interactive dashboard.

The Reading Times Dashboard displays reading times per word. The chart can be adjusted by applying filters. If the original stimuli contained words marked with an asterisk (maximally one per stimulus), the chart in the dashboard can be aligned according to those *words of interest*, using the optional command-line argument (`-a` or `--align`). Stimuli without any marked words are displayed unaligned (using the usual word index starting at 1).

In principle, this program can be used independently from `rtexp`, but note that `rtviz` needs an input `.csv` file containing reading times data and some metadata, as can be obtained from running `rtexp`.

### Install

```bash
$ pipx install git+https://github.com/kathelijnewendt/rtviz
```

### Use

For visualizing the sample data in `example_readingtimes.csv`, execute the following line to align the chart according to *words of interest*, and to run the Reading Times Dashboard (control-click the url in the terminal to view the app in a browser).
```bash
$ rtviz example_readingtimes.csv --align
```
