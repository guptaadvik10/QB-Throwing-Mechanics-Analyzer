import { View, Text, StyleSheet, Pressable, ScrollView } from "react-native"
import { useState, useEffect } from "react"
import { VideoView, useVideoPlayer } from "expo-video"

export default function History() {
    const [analyses, setAnalyses] = useState<any[]>([])
    const [currentIndex, setCurrentIndex] = useState(0)

    useEffect(() => {
        async function loadAnalyses() {
            const response = await fetch("http://localhost:8000/analyses");
            const data = await response.json();

            setAnalyses(data);
        }
        
        loadAnalyses();
    }, [])

    if (analyses.length===0) {
        return (
            <View>
                <Text>Loading Analyses...</Text>
            </View>
        )
    }

    const currentAnalysis = analyses[currentIndex]


    return (
        <ScrollView contentContainerStyle={styles.container} >
            <Text style={styles.title}>History</Text>
            <Text style={styles.subtitle}>
                Review Recent throwing Analyses
            </Text>

            <Text style={styles.counter}> Throw {currentIndex+1} of {analyses.length}</Text>

            <View style={styles.card}>
                <View style={styles.videoSide}>
                    <Text style={styles.videoName}> {currentAnalysis.video_name}</Text>
                    <AnalysisVideo url={currentAnalysis.annotated_video_url} />
                </View>
    
                <View style = {styles.metricGrid}>
                    <View style = {styles.metricCard}>
                        <Text style={styles.metricLabel}>Arm slot</Text>
                        <Text style={styles.metricValue}>{currentAnalysis.arm_slot?.toFixed(3)}°</Text>
                    </View>
                    <View style = {styles.metricCard}>
                        <Text style={styles.metricLabel}>Elbow ROM</Text>
                        <Text style={styles.metricValue}>{currentAnalysis.elbow_rom?.toFixed(3)}°</Text>
                    </View>
                    <View style = {styles.metricCard}>
                        <Text style={styles.metricLabel}>Torso Tilt</Text>
                        <Text style={styles.metricValue}>{currentAnalysis.torso_tilt?.toFixed(3)}°</Text>
                    </View>
                    <View style = {styles.metricCard}>
                        <Text style={styles.metricLabel}>Elbow Height</Text>
                        <Text style={styles.metricValue}>{currentAnalysis.elbow_height?.toFixed(3)}</Text>
                    </View>
                </View>
               
            </View>

            <View style={styles.arrows}>
                <View>
                    <Pressable 
                        onPress={() => setCurrentIndex(currentIndex-1)}
                        disabled={currentIndex  === 0}
                    >
                        <Text style={styles.arrow}>←</Text>
                    </Pressable>
                </View>
                <View>
                    <Pressable 
                        onPress={() => setCurrentIndex(currentIndex+1)}
                        disabled={currentIndex === analyses.length-1}
                    >
                        <Text style={styles.arrow} >→</Text>
                    </Pressable>
                </View>
            </View>
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


const styles = StyleSheet.create({
    container:{
        paddingBottom: 80,
        paddingHorizontal: 30,
        flexGrow: 1
    
    }, 

    title: {
        paddingTop: 40,
        padding: 30,
        fontSize: 28, 
        fontWeight: "bold", 
        textAlign: "center",
        color: "#F7F5FF",
    }, 

    subtitle: {
        fontSize: 16, 
        color: "#A8A1C2", 
        fontWeight: "500", 
        alignSelf: "center"
    }, 

    counter: {
        marginTop: 30, 
        fontSize: 18,
        padding: 20, 
        color: "#A8A1C2",
        fontWeight: "bold",
        marginLeft: 500
    }, 

    videoName: {
        fontSize: 20,
        fontWeight: "bold",
        marginBottom: 10,
        display: "none"
      },

    arrows: {
        flexDirection: "row", 
        marginTop: 20, 
        width: "100%", 
        maxWidth: 900, 
        marginBottom: 30, 
        justifyContent: "center", 
        alignSelf: "center", 
        gap: 100
    }, 

 
    arrow: {
        fontSize: 32, 
        color: "white",
        padding: 20, 
        backgroundColor: "#4B3F72",
        borderRadius: 40
    }, 

    video: {
        width: 360, 
        height: 640,
        alignSelf: "center", 
        margin: 20
    }, 

    metricCard:{
        width: "48%", 
        padding: 18, 
        marginBottom: 12, 
        borderRadius: 14, 
        backgroundColor: "#30294e",
        marginHorizontal: 10, 

        shadowColor: "#000", 
        shadowOffset: {width: 2, height: 8}, 
        shadowOpacity: 0.3, 
        shadowRadius: 12,

        borderColor: "#4A4268", 
        borderWidth: 5

  
    },
  
    metricLabel: {
      fontSize: 15, 
      marginBottom: 10, 
      color: "#A8A1C2"
    }, 
  
    metricValue: {
      fontSize: 18, 
      fontWeight: "bold", 
      color: "#F7F5FF",
      marginTop: 6
    }, 

    card: {
        flexDirection: "row", 
        gap: 28, 
        alignItems: "center", 
        paddingLeft: 30,
 
        backgroundColor: "#211D38",
        borderRadius: 18,
        borderColor: "#4A4268",
        borderWidth: 10,
  

        maxWidth: 1100,
        alignSelf: "center",
 
        shadowColor: "#000", 
        shadowOffset: {width: 4, height: 12}, 
        shadowOpacity: 0.3, 
        shadowRadius: 12
     }, 

    metricGrid: {
        width: 460,
        flexDirection: "column", 
        flexWrap: "wrap", 
        gap: 16
      }, 

    videoSide: {
        width: 360,
    }

})