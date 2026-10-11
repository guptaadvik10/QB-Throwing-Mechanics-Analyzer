import { View, Text, Button, StyleSheet, Pressable, ScrollView, ActivityIndicator} from "react-native";
import { router } from "expo-router"

export default function HomeScreen() {
  return (
    <View style = {styles.container}>
      <Text style={styles.title}> QB Analyzer </Text>
      <Text style={styles.welcome}> Welcome Back</Text>
      <Text style={styles.subtitle}> Analyze, Understand, and Compare throwing mechnanics </Text>
      
      
    </View>

  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1, 
    marginHorizontal: 25
  }, 

  welcome: {
    fontSize: 25, 
    fontWeight: 'bold', 
    marginVertical: 20, 
    textAlign: "center"
  }, 

  title: {
    fontSize: 30, 
    fontWeight: "bold",
    marginVertical: 10, 
    textAlign: "center"
  }, 

  subtitle: {
    fontSize: 16, 
    marginTop: 10, 
    marginBottom: 20, 
    textAlign: "center",
    fontWeight: "500"
  }, 

})

