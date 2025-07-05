import React, { useRef, useEffect, useState } from 'react';
import { 
  View, 
  PanGestureHandler, 
  State,
  Dimensions 
} from 'react-native';
import { PanGestureHandler as RNGHPanGestureHandler } from 'react-native-gesture-handler';
import Animated, { 
  useAnimatedGestureHandler,
  useAnimatedStyle,
  useSharedValue,
  runOnJS,
  withDecay
} from 'react-native-reanimated';
import RouletteCard from './RouletteCard';
import { PREMIUM_MENU_DATA } from '../data/MenuData';
import { RoulettePhysicsEngine, PHYSICS } from '../utils/PhysicsEngine';

const { width: screenWidth, height: screenHeight } = Dimensions.get('window');

const RouletteWheel = ({ onSpinEnd }) => {
  const rotation = useSharedValue(0);
  const [physicsEngine] = useState(() => new RoulettePhysicsEngine());
  
  // 룰렛 크기 계산 (화면에 맞게 조정)
  const wheelSize = Math.min(screenWidth, screenHeight) * 0.8;
  const centerX = screenWidth / 2;
  const centerY = screenHeight / 2;
  
  const cardSize = {
    width: wheelSize * 0.15,
    height: wheelSize * 0.2,
    radius: wheelSize * 0.35
  };

  useEffect(() => {
    physicsEngine.start();
    return () => physicsEngine.stop();
  }, []);

  // 물리 엔진 상태를 애니메이션과 동기화
  const updateRotation = (newRotation) => {
    rotation.value = newRotation;
  };

  const gestureHandler = useAnimatedGestureHandler({
    onStart: (_, context) => {
      context.startRotation = rotation.value;
      runOnJS(physicsEngine.startDrag.bind(physicsEngine))(0, 0, centerX, centerY);
    },
    onActive: (event, context) => {
      // 드래그 시 회전 계산
      const { translationX, translationY } = event;
      const dragAngle = Math.atan2(translationY, translationX) * (180 / Math.PI);
      const deltaRotation = dragAngle * 0.5; // 드래그 감도 조정
      
      rotation.value = context.startRotation + deltaRotation;
      
      runOnJS(physicsEngine.updateDrag.bind(physicsEngine))(
        centerX + translationX, 
        centerY + translationY, 
        centerX, 
        centerY
      );
    },
    onEnd: (event) => {
      runOnJS(physicsEngine.endDrag.bind(physicsEngine))();
      
      // 관성 적용
      const velocity = Math.sqrt(event.velocityX ** 2 + event.velocityY ** 2) * 0.001;
      rotation.value = withDecay({
        velocity: velocity,
        clamp: [-360, 360],
        deceleration: 0.998
      });
    }
  });

  const animatedStyle = useAnimatedStyle(() => {
    return {
      transform: [{ rotate: `${rotation.value}deg` }]
    };
  });

  // 랜덤 스핀 함수
  const randomSpin = () => {
    const randomRotation = Math.random() * 1440 + 720; // 2~4바퀴 회전
    rotation.value = withDecay({
      velocity: randomRotation * 0.01,
      deceleration: 0.998
    });
    physicsEngine.spin();
  };

  return (
    <View style={{
      width: wheelSize,
      height: wheelSize,
      position: 'absolute',
      left: centerX - wheelSize / 2,
      top: centerY - wheelSize / 2
    }}>
      <RNGHPanGestureHandler onGestureEvent={gestureHandler}>
        <Animated.View style={[
          {
            width: wheelSize,
            height: wheelSize,
            borderRadius: wheelSize / 2,
            backgroundColor: '#ffffff',
            justifyContent: 'center',
            alignItems: 'center',
            shadowColor: '#000',
            shadowOffset: { width: 0, height: 4 },
            shadowOpacity: 0.3,
            shadowRadius: 8,
            elevation: 10
          },
          animatedStyle
        ]}>
          {/* 중앙 원 */}
          <View style={{
            width: wheelSize * 0.1,
            height: wheelSize * 0.1,
            borderRadius: wheelSize * 0.05,
            backgroundColor: '#667eea',
            position: 'absolute',
            zIndex: 10,
            shadowColor: '#000',
            shadowOffset: { width: 0, height: 2 },
            shadowOpacity: 0.3,
            shadowRadius: 4,
            elevation: 5
          }} />
          
          {/* 카드들 */}
          {PREMIUM_MENU_DATA.map((item, index) => (
            <RouletteCard
              key={`${item.id}-${index}`}
              item={item}
              index={index}
              totalCards={PREMIUM_MENU_DATA.length}
              cardSize={cardSize}
            />
          ))}
        </Animated.View>
      </RNGHPanGestureHandler>
    </View>
  );
};

export default RouletteWheel;