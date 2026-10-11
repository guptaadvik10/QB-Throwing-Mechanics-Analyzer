import { View, Text, Button, StyleSheet, Pressable, ScrollView, ActivityIndicator} from "react-native";
import {useState, useEffect} from "react"
import * as DocumentPicker from "expo-document-picker"
import {VideoView, useVideoPlayer} from "expo-video"


export default function Analyze() {

  const  [video, setVideo] = useState<any>(null);
  const  [metrics, setMetrics] = useState<any>(null);
  const [annotatedVideoUrl, setAnnotatedVideoUrl] = useState<string | null>(null)
  const player = useVideoPlayer(annotatedVideoUrl)
  const [screenState, setScreenState] = useState("upload")

  const [coachAnalysis, setCoachAnalysis] = useState<any>(null)

  useEffect(() => {
    if (annotatedVideoUrl) {
      player.replaceAsync(annotatedVideoUrl)
    }
  }, [annotatedVideoUrl])

  const pickVideo = async () => {
    const result = await DocumentPicker.getDocumentAsync({
      type: "video/*"
    });
    if (!result.canceled) {
      setVideo(result.assets[0])
    }
  }

  const analyzeVideo = async () => {
    if (video) {
      const formData = new FormData();

      formData.append("file", video.file)

      setScreenState("analyze")

      const response = await fetch("http://localhost:8000/analyze", 
        {method: "POST", 
        body: formData
     })
      const data = await response.json();

      setMetrics(data.metrics)
      setAnnotatedVideoUrl(
        `${data.annotated_video_url}?t=${Date.now()}`
      );

      if (data.metrics == null) {
        setMetrics("bad video")
      }
      setScreenState("results")
      setCoachAnalysis(data.coach_analysis)
    }


  }
  
  return (
    <ScrollView style={styles.container}>  

      {screenState === "upload" && (
        <View>
          <Text style={styles.title}>Qb Analyzer</Text>

          <Pressable
            style={styles.buttonContainer}
            onPress={pickVideo}
          >
          <Text style={styles.pressableText}>Select Video</Text>
          </Pressable>
          {video && (<Pressable 
            style = {styles.buttonContainer}
            onPress = {analyzeVideo}
          > 
          <Text style = {styles.pressableText}>Analyze Video</Text>
          </Pressable>
          )}
        </View>
      )}

      {screenState === "analyze" && (
        <View style = {styles.loadingContainer}>

          <ActivityIndicator size = "large" />

          <Text style = {styles.loadingTitle} >Analyzing Throw....</Text>

          <Text style = {styles.loadingSubtitle}> Detecting motion and mechanics</Text>

        </View>
      )}
      
      
      {screenState === "results" && (
        <View>

            <Text style= {styles.title}> Throw Analysis </Text>

            <View style={styles.analysisGrid}> 

                <View style={styles.videoColumn}>
                    <View style={styles.videoCard}> 
                        {annotatedVideoUrl && (
                            <VideoView
                            player = {player}
                            style = {styles.video}
                            nativeControls
                            contentFit = "contain"
                            />
                        )}
                    </View>
                </View>
        
                
                <View style = {styles.metricColumn}>
                     <Text style = {styles.sectionText}> Key Metrics</Text>

                    {metrics && (
                    <View style = {styles.metricGrid}>
                        
                        <View style = {styles.metricCard}>
                        <Text style={styles.metricLabel}>Max Elbow Angle</Text>
                        <Text style={styles.metricValue}>{metrics.max_elbow_angle?.toFixed(1)}°</Text>
                        </View>

                        <View style = {styles.metricCard}>
                        <Text style={styles.metricLabel}>Min Elbow Angle</Text>
                        <Text style={styles.metricValue}>{metrics.min_elbow_angle?.toFixed(1)}°</Text>
                        </View>

                        <View style = {styles.metricCard}>
                        <Text style={styles.metricLabel}>Elbow Range of Motion</Text>
                        <Text style={styles.metricValue}>{metrics.elbow_rom?.toFixed(1)}°</Text>
                        </View>

                        <View style = {styles.metricCard}>
                        <Text style={styles.metricLabel}>Elbow Velocity</Text>
                        <Text style={styles.metricValue}>{metrics.release_velocity?.toFixed(1)}°</Text>
                        </View>

                        <View style={styles.metricCard}>
                        <Text style={styles.metricLabel}>Shoulder Abduction</Text>
                        <Text style={styles.metricValue}>
                            {metrics.shoulder_abduction?.toFixed(1)}°
                        </Text>
                        </View>

                        <View style = {styles.metricCard}>
                        <Text style={styles.metricLabel}>Elbow Height</Text>
                        <Text style={styles.metricValue}>{metrics.elbow_height?.toFixed(1)}</Text>
                        </View>

                        <View style = {styles.metricCardWide}>
                        <Text style={styles.metricLabel}>Torso Tilt</Text>
                        <Text style={styles.metricValue}>{metrics.torso_tilt?.toFixed(1)}°</Text>
                        </View>

                        <View style = {styles.metricCardWide}>
                            <View style={styles.armSlotLayout}> 
                                <View style={styles.armSlotMetric}>
                                    <Text style={styles.metricLabel}>Arm Slot</Text>
                                    <Text style={styles.metricValue}>{metrics.arm_slot?.toFixed(1)}°</Text>
                                </View>
                                <Text style={styles.metricValue}> {metrics.arm_slot_class} </Text>
                            </View>
            
                        </View>

                    </View>
                    )}

                </View>
            </View>
            {coachAnalysis && (
                    <View style = {styles.aiAnalysisGrid}>

                        <Text style = {styles.aiTextHeader}> AI Throw Analysis </Text>

                        <View style = {styles.aiPanel}>
                            <Text style={styles.aiText}> {coachAnalysis.summary}</Text>
                        </View>

                        <Text style = {styles.aiTextHeader}>  Key Observations </Text>

                        <View style = {styles.aiPanel}>
                            {coachAnalysis.strengths.map(
                                (item: string, index: number) => (
                                    <Text key={index} style={styles.aiText} > • {item} </Text>
                                )
                            )}
                        </View>
                    
                        <Text style = {styles.aiTextHeader}> Things to Watch </Text>

                        <View style = {styles.aiPanel}>
                            {coachAnalysis.things_to_watch.map(
                                (item: string, index: number) => (
                                    <Text 
                                    key={index}
                                        style={styles.aiText}> 
                                        • {item}
                                    </Text>
                                )
                            )}
                        </View>


                    </View>
                )}
        </View>
      )}

       
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
    backgroundColor: "#17152B",
  }, 

  title: {
    padding: 30,
    fontSize: 28, 
    fontWeight: "bold", 
    marginBottom: 20,
    textAlign: "center",
    color: "#F7F5FF",
  }, 

  analysisGrid: {
    width: "100%", 
    maxWidth: 1350, 
    alignSelf: "flex-start", 
    flexDirection: "row", 
    gap: 40, 
    alignItems: "flex-start"
  },

  videoCard: {
    width: "100%",
    maxWidth: 450,

    backgroundColor: "#1B1830", 
    borderRadius: 24, 
    padding: 30, 

    borderWidth: 5, 
    borderColor: "#342D55", 

    shadowColor: "#000", 
    shadowOffset: { width: 4, height: 12 }, 
    shadowOpacity: 0.4, 
    shadowRadius: 12, 
  },

  videoColumn: {
    flex: 0.8, 
    minWidth: 0, 
    alignItems: "center"
  },

  video: {
    width: "100%", 
    aspectRatio: 9/16, 
    borderRadius: 16, 
  }, 

  buttonContainer: {
    backgroundColor: "#F59E42", 
    paddingVertical: 13.5, 
    paddingHorizontal: 10, 
    borderRadius: 10, 
    width: 250, 
    alignSelf: "center",
    margin: 10,

    shadowColor: "#000", 
    shadowOffset: { width: 0, height: 8 }, 
    shadowOpacity: 0.5, 
    shadowRadius: 12, 

  }, 
  
  pressableText: {
    fontSize: 20, 
    fontWeight: "bold", 
    textAlign: "center"
  }, 

  loadingContainer: {
    alignItems: "center", 
    marginTop: 150
  }, 

  loadingTitle: {
    fontSize: 24, 
    fontWeight: "bold", 
    marginTop: 20,
    color: "#F7F5FF"
  }, 

  loadingSubtitle: {
    fontSize: 16, 
    marginTop: 10,
    color: "#F7F5FF"
  }, 

  metricColumn: {
    flex: 1.2, 
    minWidth: 0, 
    flexDirection: "column", 
    alignItems: "flex-start"
  },

  metricGrid: { 
    width: "100%", 
    flexWrap: "wrap",
    gap: 30, 
    flexDirection: "row"
  }, 

  metricCard:{
    width: "45%", 
    padding: 18, 
    borderRadius: 12, 
    backgroundColor: "#25203F", 
    borderColor: "#342D55", 

    shadowColor: "#000", 
    shadowOffset: { width: 0, height: 8 }, 
    shadowOpacity: 0.2, 
    shadowRadius: 12, 

  },

  metricCardWide: {
    width: "94%",
    padding: 18, 
    borderRadius: 12, 
    backgroundColor: "#25203F", 
    borderColor: "#342D55", 

    shadowColor: "#000", 
    shadowOffset: { width: 0, height: 8 }, 
    shadowOpacity: 0.2, 
    shadowRadius: 12, 
  },

  metricLabel: {
    fontSize: 15, 
    marginBottom: 10, 
    color: "#A8A1C2"
  }, 

  metricValue: {
    color: "#F7F5FF",
    fontSize: 18, 
    fontWeight: "bold", 
    marginTop: 6
  }, 

  armSlotLayout: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "flex-start"
  },

  armSlotMetric: {
    marginRight: 55
  },

  sectionText: {
    color: "#F7F5FF",
    fontSize: 25,
    fontWeight: "bold", 
    textAlign: "center", 
    marginBottom: 40, 
    marginTop: 40
  }, 

  aiAnalysisGrid: {
    alignSelf: "flex-start"
  }, 

  aiText: {
    fontSize: 15, 
    color: "#A8A1C2",
    fontWeight: "600", 
    lineHeight: 26, 

  }, 

  aiTextHeader: {
    fontSize: 22, 
    color: "white",
    fontWeight: "bold", 
    padding: 30,
    paddingHorizontal: 80
  }, 

  aiPanel: {
    backgroundColor: "#25203F", 
    padding: 20, 
    borderRadius: 12, 
    borderColor: "#342D55", 
    width: "70%",
    marginHorizontal: 20,

    shadowColor: "#000", 
    shadowOffset: {width: 4, height: 10},
    shadowOpacity: 0.3, 
    shadowRadius: 12, 
  }

})