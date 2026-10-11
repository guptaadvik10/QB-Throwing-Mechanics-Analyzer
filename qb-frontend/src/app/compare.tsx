import { View, Text, Pressable, StyleSheet, ScrollView } from "react-native";
import { useState, useEffect } from "react"
import {VideoView, useVideoPlayer} from "expo-video"
import Svg, {
    Polyline,
    Line,
    Text as SvgText
  } from "react-native-svg";


export default function Compare() {
    const [analyses, setAnalyses] = useState<any[]>([])
    const [throwAId, setThrowAId] = useState<number | null>(null);
    const [throwBId, setThrowBId] = useState<number | null>(null);
    const [comparison, setComparison] = useState<any>(null);

    useEffect(() => {
        fetch("http://localhost:8000/analyses")
            .then((response) => response.json())
            .then((data) => setAnalyses(data))
    }, [])

    const compareThrows = async () => {
        if (throwAId === null || throwBId === null) {
            return;
        }

        const response = await fetch(
            `http://localhost:8000/compare/${throwAId}/${throwBId}`)


        const data = await response.json();
        console.log(JSON.stringify(data, null, 2));
        setComparison(data);

    }

    const chartWidth = 800;
    const chartHeight = 300;
    const padding = 40;

    function makePoints(series: any[]) {
        return series
          .map((point) => {
            const x =
              padding +
              (point.standardized / 100) *
                (chartWidth - 2 * padding);
      
            const y =
              chartHeight -
              padding -
              (point.elbow_angle_smoothed / 180) *
                (chartHeight - 2 * padding);
      
            return `${x},${y}`;
          })
          .join(" ");
      }

      if (comparison) {
        console.log(
          "A FIRST POINT:",
          comparison.throw_a.throw_series[0]
        );
      
        console.log(
          "A POINTS:",
          makePoints(comparison.throw_a.throw_series)
        );
      }
    

    return (
        <ScrollView>
            <Text style={styles.title}>Compare Throws</Text>
            <View style={styles.selectionRow}>
                <View style={styles.selectionColumn}>
                    <Text style={styles.selectionTitle}>Throw A</Text>

                    {analyses.map((analysis) => (

                        <Pressable 
                            key={`a-${analysis.id}`}
                            onPress={() => setThrowAId(analysis.id)}
                        >
                            <Text style={styles.throwOption}>
                                {analysis.video_name}
                                {throwAId === analysis.id ? " ✓" : ""}
                            </Text>
                        </Pressable>
                    ))}
                </View>

                <View style={styles.selectionColumn}>
                    <Text style={styles.selectionTitle}>Throw B</Text>

                    {analyses.map((analysis) => (
                    <Pressable
                        key={`b-${analysis.id}`}
                        onPress={() => setThrowBId(analysis.id)}
                    >
                        <Text style={styles.throwOption}>
                            {analysis.video_name}
                            {throwBId === analysis.id ? " ✓" : ""}
                        </Text>
                    </Pressable>
                    ))}

                </View>
        
            </View>
            <View style={styles.compareButton}>
                <Pressable onPress={compareThrows}>
                    <Text style={styles.compareSubtitle} >Compare Throws</Text>
                </Pressable> 
            </View>



            {comparison && (
            
                <View style={styles.results}> 

                    <View style={styles.videoRow}>
                        <View style={styles.throwResultColumn} >
                            <Text style= {styles.resultsSubtitle}> Throw A</Text>
                            <AnalysisVideo url={comparison.throw_a.annotated_video_url} />
                            <View style = {styles.metricsGroup}>

            
                                    <View style={styles.metricCard}>
                                        <Text style={styles.metricLabel}>Arm Slot</Text>
                                        <Text style={styles.metricValue}>
                                            {comparison.throw_a.metrics.arm_slot?.toFixed(1)}°
                                        </Text>
                                    </View>
                               
                                    <View style={styles.metricCard}>
                                        <Text style={styles.metricLabel}>Elbow ROM</Text>
                                        <Text style={styles.metricValue}>
                                            {comparison.throw_a.metrics.elbow_rom?.toFixed(1)}°
                                        </Text>
                                    </View>
                               
                                    <View style={styles.metricCard}>
                                        <Text style={styles.metricLabel}>Torso Tilt</Text>
                                        <Text style={styles.metricValue}>
                                            {comparison.throw_a.metrics.torso_tilt?.toFixed(1)}°
                                        </Text>
                                    </View>
                               
                                    <View style={styles.metricCard}>
                                        <Text style={styles.metricLabel}>Elbow Height</Text>
                                        <Text style={styles.metricValue}>
                                            {comparison.throw_a.metrics.elbow_height?.toFixed(1)}°
                                        </Text>
                                    </View>

                            </View>

                            
                        </View>

                        

                        <View style={styles.throwResultColumn} >
                            <Text style= {styles.resultsSubtitle}> Throw B</Text>
                            <AnalysisVideo url={comparison.throw_b.annotated_video_url} />

                            <View style = {styles.metricsGroup}>

            
                                <View style={styles.metricCard}>
                                    <Text style={styles.metricLabel}>Arm Slot</Text>
                                    <Text style={styles.metricValue}>
                                        {comparison.throw_b.metrics.arm_slot?.toFixed(1)}°
                                    </Text>
                                </View>

                                <View style={styles.metricCard}>
                                    <Text style={styles.metricLabel}>Elbow ROM</Text>
                                    <Text style={styles.metricValue}>
                                        {comparison.throw_b.metrics.elbow_rom?.toFixed(1)}°
                                    </Text>
                                </View>

                                <View style={styles.metricCard}>
                                    <Text style={styles.metricLabel}>Torso Tilt</Text>
                                    <Text style={styles.metricValue}>
                                        {comparison.throw_b.metrics.torso_tilt?.toFixed(1)}°
                                    </Text>
                                </View>

                                <View style={styles.metricCard}>
                                    <Text style={styles.metricLabel}>Elbow Height</Text>
                                    <Text style={styles.metricValue}>
                                        {comparison.throw_b.metrics.elbow_height?.toFixed(1)}°
                                    </Text>
                                </View>

                            </View>
                            
                            
                            
                        </View>
                    </View>

                <Text style={styles.sectionTitle}> Key Differences </Text>
                
                <View style = {styles.comparisionMetrics}>


                    <View style = {styles.comparisionBox}>
                        <Text style = {styles.comparisionText}>
                            {getDirectionalText(
                                comparison.comparison.arm_slot.comparison,
                                "arm slot"
                            )}
                        </Text>
                    </View>
                
                    <View style = {styles.comparisionBox}>
                        <Text style = {styles.comparisionText}>
                            {getDirectionalText(
                                comparison.comparison.elbow_rom.comparison,
                                "elbow ROM"
                            )}
                        </Text>
                    </View>
                    
                    <View style = {styles.comparisionBox}>
                        <Text style = {styles.comparisionText}>
                            {getDirectionalText(
                                comparison.comparison.torso_tilt.comparison,
                                "torso tilt"
                            )}
                        </Text>
                    </View>
            
                    <View style = {styles.comparisionBox}>
                        <Text style = {styles.comparisionText}>
                            {getDirectionalText(
                                comparison.comparison.elbow_height.comparison,
                                "elbow height"
                            )}
                        </Text>
                    </View>

                </View>
                
                <View style={styles.graphContainer}>
                    <Text style={styles.sectionTitle}>
                        Elbow Angle Through Throw
                    </Text>

                    <Svg
                        width="100%"
                        height={300}
                        viewBox={`0 0 ${chartWidth} ${chartHeight}`}
                    >
                        {/* Y axis */}
                        <Line
                        x1={padding}
                        y1={padding}
                        x2={padding}
                        y2={chartHeight - padding}
                        stroke="#A8A1C2"
                        strokeWidth={1}
                        />

                        {/* X axis */}
                        <Line
                        x1={padding}
                        y1={chartHeight - padding}
                        x2={chartWidth - padding}
                        y2={chartHeight - padding}
                        stroke="#A8A1C2"
                        strokeWidth={1}
                        />

                        {/* Throw A */}
                        <Polyline
                        points={makePoints(
                            comparison.throw_a.throw_series
                        )}
                        fill="none"
                        stroke="#FF9F40"
                        strokeWidth={4}
                        />

                        {/* Throw B */}
                        <Polyline
                        points={makePoints(
                            comparison.throw_b.throw_series
                        )}
                        fill="none"
                        stroke="#8B7CFF"
                        strokeWidth={4}
                        />

                        <SvgText
                        x={padding}
                        y={chartHeight - 10}
                        fill="#A8A1C2"
                        fontSize="14"
                        >
                        0%
                        </SvgText>

                        <SvgText
                        x={chartWidth - padding - 30}
                        y={chartHeight - 10}
                        fill="#A8A1C2"
                        fontSize="14"
                        >
                        100%
                        </SvgText>
                    </Svg>
                    </View>
            

                </View>

            )}

        </ScrollView>
      
    )
}

function AnalysisVideo({url}: {url:string}){
    const player = useVideoPlayer(
        url, 
        player => {
            player.loop = true;
        }
    )

    return (
        <VideoView   
            player = {player}
            style={styles.video}
            contentFit="contain"
            nativeControls
        />
    )
}

function getDirectionalText(
    diff: number,
    label: string
  ) {
    if (diff > 0) {
      return `Throw A has a ${Math.abs(diff).toFixed(1)}° higher ${label}`;
    }
  
    if (diff < 0) {
      return `Throw B has a ${Math.abs(diff).toFixed(1)}° higher ${label}`;
    }
  
    return `${label} is the same for both throws`;
  }

const styles = StyleSheet.create({
    title: {
        padding: 30,
        fontSize: 28, 
        fontWeight: "bold", 
        marginBottom: 20,
        textAlign: "center",
        color: "#F7F5FF",
    },

    selectionRow: {
        flexDirection: "row", 
        gap: 24, 
        width: "100%",
        paddingBottom: 20,
        justifyContent: "center",
        alignItems: "flex-start",

    },

    selectionColumn: {
        flex: 1, 
        alignItems: "center", 
        maxWidth: 500,

        backgroundColor: "#211E3A",
        borderRadius: 20, 
        padding: 20, 
        borderWidth: 3, 
        borderColor: "#343052"
    }, 

    selectionTitle: {
        fontSize: 17, 
        fontWeight: "700", 
        paddingBottom: 15,
        color: "#F7F5FF",
    }, 

    throwOption: {
        color: "#A8A1C2",
        paddingBottom: 5
    },

    compareSubtitle: {
        alignSelf: "center", 
        fontSize: 17,
        fontWeight: "bold"
    }, 

    compareButton: {
        marginTop: 20,
        backgroundColor: "#F59E42",
        padding: 20, 
        width: 250, 
        alignSelf: "center", 
        
        borderRadius: 20,
        shadowColor: "#000", 
        shadowOffset: {width: 1, height: 5}, 
        shadowOpacity: 0.4, 
        shadowRadius: 10
    }, 



    results: {
   
        width: "100%",
        paddingBottom: 20,

    },

    videoRow: {
        width: "100%",
        maxWidth: 1100,
        alignSelf: "center",
        flexDirection: "row",
        gap: 1,
        justifyContent: "center"
    },

    throwResultColumn: {
        flex: 1,
        alignItems: "center",
    },

    video: {
       width: "100%", 
       maxWidth: 360, 
       aspectRatio: 9/16, 
       alignSelf: "center", 
       borderRadius: 8
    }, 

   resultsSubtitle: {
        fontSize: 17, 
        fontWeight: "700", 
        paddingVertical: 40,
        color: "#F7F5FF",
   }, 

 

   metricCard: {
        backgroundColor: "#25203F",
        borderRadius: 14,
        padding: 16,
        borderWidth: 4,
        borderColor: "#342D55",
        width: "48%", 

        shadowColor: "#000", 
        shadowOffset: {width: 1, height: 5}, 
        shadowOpacity: 0.4, 
        shadowRadius: 10
   }, 

   metricLabel: {
        color: "#A8A1C2",
        fontSize: 14,
  },
  
  metricValue: {
        color: "#F7F5FF",
        fontSize: 20,
        fontWeight: "700",
        marginTop: 6,
  },

  metricsGroup: {
   
        width: "100%",
        maxWidth: 360,
        marginTop: 18,
        gap: 12,
        flexDirection: "row", 
        flexWrap: "wrap"
   
  }, 

  allMetrics: {
    flexDirection: "row"
  }, 

  comparisionMetrics: {
    alignItems: "center",
    marginTop: 30, 
    gap: 20, 
    padding: 10, 
    flexDirection: "row",
    justifyContent: "center"
  }, 

  comparisionBox: {
    padding: 15, 
    backgroundColor: "#25203F", 
    borderColor: "#342D55", 
    borderWidth: 4, 
    borderRadius: 15,
    flexDirection: "row",
    flex: 1, 
    minWidth: 240,
    maxWidth: 350,

    shadowColor: "#000", 
    shadowRadius: 4, 
    shadowOffset: {width: 2, height: 8}, 
    shadowOpacity: 0.3

  }, 

  comparisionText: {
    fontSize: 16, 
    color: "#F7F5FF", 
    fontWeight: 600, 
    textAlign: "center", 
    alignSelf: "center"

  }, 

  sectionTitle: {
    fontSize: 20, 
    fontWeight: "700", 
    padding: 15,
    color: "#F7F5FF",
    alignSelf: "center", 
    marginTop: 30

  },

  graphContainer: {
    width: "100%",
    maxWidth: 1000,
    height: 400,
    alignSelf: "center",
    marginTop: 40,
  }


})

