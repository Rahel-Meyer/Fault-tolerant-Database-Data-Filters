## which n ist best?

### FP vs. FN without second dataset

| Variables                                                                                         | Methods                                                          | Graphs                        |
|---------------------------------------------------------------------------------------------------|------------------------------------------------------------------|-------------------------------|
| N = 10 000<br/> min_length = 5<br/> max_length = 10<br/> error Probability range (0.0, 0.5, 0.05) | Data = alphabetic<br/> Filter = normal <br/> corruption = normal | ![Figure_1.png](Figure_1.png) |
| N = 10 000<br/> min_length = 5<br/> max_length = 10<br/> error Probability range (0.0, 0.5, 0.05) | Data = numeric<br/> Filter = normal <br/> corruption = normal    | ![Figure_2.png](Figure_2.png) |
| N = 10 000<br/> min_length = 5<br/> max_length = 10<br/> error Probability range (0.0, 0.5, 0.05) | Data = printable<br/> Filter = normal <br/> corruption = normal  | ![Figure_3.png](Figure_3.png) |
| error Probability range (0.0, 0.5, 0.05) | Data = tpc-h<br/> Filter = normal <br/> corruption = normal      | ![Figure_7.png](Figure_7.png) |


For numeric data n=1 an n=2 have very little FN compared to n=3. <br/>
Alphabetic and printable data have the most FP at n=2. Filter not rough enough like n=1 but also not specific enough like n=3.  <br/>
Number of FP the highest at low error probability, then decreases. Few errors lead to different matches. <br/>
Tpc-h result more similar to numeric result, although data is mixed numeric and alphabetic. Why? Maybe some percentage of numerical Data leads to this behaviour?

### FP vs. FN with second dataset

| Variables                                                                                         | Methods                                                          | Graphs                        |
|---------------------------------------------------------------------------------------------------|------------------------------------------------------------------|-------------------------------|
| N = 10 000<br/> min_length = 5<br/> max_length = 10<br/> error Probability range (0.0, 0.5, 0.05) | Data = alphabetic<br/> Filter = normal <br/> corruption = normal | ![Figure_4.png](Figure_4.png) |
| N = 10 000<br/> min_length = 5<br/> max_length = 10<br/> error Probability range (0.0, 0.5, 0.05) | Data = numeric<br/> Filter = normal <br/> corruption = normal    | ![Figure_5.png](Figure_5.png) |
| N = 10 000<br/> min_length = 5<br/> max_length = 10<br/> error Probability range (0.0, 0.5, 0.05) | Data = printable<br/> Filter = normal <br/> corruption = normal  | ![Figure_6.png](Figure_6.png) |

Similar behavior, but worse.  <br/>
How could this be mathematically described?

## FP vs. FN with redundant Prefixes

The Filter has the most common prefixes more than once. <br/>
The results aren't better $\rightarrow$ calculation of the Confusionmatrix is wrong? More redundancy?

| Variables                                                                                         | Methods                                                             | Graphs                          |
|---------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|---------------------------------|
| N = 10 000<br/> min_length = 5<br/> max_length = 10<br/> error Probability range (0.0, 0.5, 0.05) | Data = alphabetic<br/> Filter = redundant <br/> corruption = normal | ![Figure_8.png](Figure_8.png)   |
| N = 10 000<br/> min_length = 5<br/> max_length = 10<br/> error Probability range (0.0, 0.5, 0.05) | Data = numeric<br/> Filter = redundant <br/> corruption = normal    | ![Figure_9.png](Figure_9.png)   |
| N = 10 000<br/> min_length = 5<br/> max_length = 10<br/> error Probability range (0.0, 0.5, 0.05) | Data = printable<br/> Filter = redundant <br/> corruption = normal  | ![Figure_10.png](Figure_10.png) |
| error Probability range (0.0, 0.5, 0.05)<br/> no second Data                                      | Data = tpc-h<br/> Filter = redundant <br/> corruption = normal      | ![Figure_11.png](Figure_11.png) |

