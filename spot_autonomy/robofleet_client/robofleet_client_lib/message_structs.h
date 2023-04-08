#pragma once
#include<cstdint>
#include<string>

struct RobofleetSubscription {
	std::string topic_regex;
	uint8_t action;
};

struct RobotLocation {
	std::string frame;
	float x;
	float y;
	float theta;
};

struct RobotStatus {
	std::string status;
	bool is_ok;
	float battery_level;
	std::string location;
};