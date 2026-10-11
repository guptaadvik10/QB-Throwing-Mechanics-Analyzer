import { View, Text, Pressable, StyleSheet, useWindowDimensions } from "react-native";
import { Stack, router, Slot } from "expo-router"

export default function RootLayout(){
  const { width } = useWindowDimensions();

  const isMobile = width < 768;
  return (
    <View style = {styles.app}>

      <View style = {styles.navBar}>

        <View style = {isMobile ? styles.navMobile : styles.navLinks}>
          
          <Pressable 
            onPress={() => router.push("/")}
            style={({ hovered }) => [
              styles.navButton, 
              hovered && styles.navButtonHovered,
            ]}
          >
            <Text style = {styles.navText}> Home </Text>
          </Pressable>

          <Pressable 
            onPress={() => router.push("/analyze")}
            style={({ hovered }) => [
              styles.navButton, 
              hovered && styles.navButtonHovered,
            ]}
          >
            <Text style = {styles.navText}> Analyze </Text>
          </Pressable>


          <Pressable 
            onPress={() => router.push("/compare")}
            style={({ hovered }) => [
              styles.navButton, 
              hovered && styles.navButtonHovered,
            ]}
          >
            <Text style = {styles.navText}> Compare </Text>
          </Pressable>


          <Pressable 
            style={({ hovered }) => [
              styles.navButton, 
              hovered && styles.navButtonHovered,
            ]}
          >
            <Text style = {styles.navText}> Sample Metrics </Text>
          </Pressable>

          <Pressable 
            style={({ hovered }) => [
              styles.navButton, 
              hovered && styles.navButtonHovered,
            ]}
          >
            <Text style = {styles.navText}> Reference Qb's </Text>
          </Pressable>

          <Pressable 
            onPress={() => router.push("/history")}
            style={({ hovered }) => [
              styles.navButton, 
              hovered && styles.navButtonHovered,
            ]}
          >
            <Text style = {styles.navText}> History </Text>
          </Pressable>

      
        </View>
      </View>

      <View style = {styles.page}>
        <Slot />
      </View>

    </View>
  );
}

const styles = StyleSheet.create({
  app: {
    flex: 1, 
  }, 
  
  navBar: {
    height: 70, 
    flexDirection: "row", 
    alignItems: "center", 
    justifyContent: "space-between", 
    paddingHorizontal: 30, 
    borderBottomWidth: 1, 
    backgroundColor: "#211E3A",
    borderBottomColor: "#343052",

  }, 

  navMobile: {
    flexDirection: "row", 
    justifyContent: "space-around", 
    alignItems: "center",
    width: "100%",
    paddingHorizontal: 12,
    paddingVertical: 10,
  },

  navLinks: {
    flexDirection: "row", 
    gap: 28, 
    alignItems: "center", 
    marginLeft: "auto", 
    padding: 20
  }, 

  navButton: {
    padding: 10,
    backgroundColor: "#2A2648",
    borderRadius: 20
  },

  navText: {
    fontSize: 14, 
    fontWeight: "500",
    color: "white"
  }, 

  navTextMobile: {
    fontSize: 16, 
    color: "#F8F7FF"
  },

  page: {
    flex: 1, 
    backgroundColor: "#17152B",
  }, 

  navButtonHovered: {
    opacity: 0.75
  }

})